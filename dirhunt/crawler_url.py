# -*- coding: utf-8 -*-
import cgi
import socket
from typing import TYPE_CHECKING, Any, Optional

from aiohttp.web_response import Response
from bs4 import BeautifulSoup
from requests import RequestException
from urllib3.exceptions import ReadTimeoutError

from dirhunt.url import Url

MAX_RESPONSE_SIZE = 1024 * 512
FLAGS_WEIGHT = {
    "blank": 4,
    "not_found.fake": 3,
    "html": 2,
}


if TYPE_CHECKING:
    from dirhunt.crawler import Crawler
    from dirhunt.processors import ProcessBase


class CrawlerUrlRequest:
    response = Optional[Response]
    content: Optional[str] = None
    _soup: Optional[BeautifulSoup] = None

    def __init__(self, crawler_url: "CrawlerUrl"):
        self.crawler_url = crawler_url
        self.crawler = crawler_url.crawler

    async def retrieve(self) -> "ProcessBase":
        from dirhunt.processors import (
            get_processor,
            Error,
        )

        text = ""
        try:
            await self.crawler.domain_semaphore.acquire(self.crawler_url.url.domain)
            pass
            async with self.crawler.session.get(
                self.crawler_url.url.url,
                verify_ssl=False,
                timeout=self.crawler.configuration.timeout,
                allow_redirects=False,
            ) as response:
                self.crawler_url.set_type(response.headers.get("Content-Type"))
                self.crawler_url.flags.add(str(response.status))
                self.response = response
                processor = get_processor(self)
                if processor and processor.requires_content:
                    encoding = response.get_encoding()
                    self.content = (
                        await response.content.read(MAX_RESPONSE_SIZE)
                    ).decode(encoding, errors="ignore")
                if processor.has_descendants:
                    processor = get_processor(self)
                # text = ""
                # soup = None
                # processor = None
                # if response.status_code < 300 and self.must_be_downloaded(response):
                #     try:
                #         text = response.raw.read(MAX_RESPONSE_SIZE, decode_content=True)
                #     except (RequestException, ReadTimeoutError, socket.timeout) as e:
                #         self.crawler.current_processed_count += 1
                #         self.crawler.results.put(Error(self, e))
                #         self.close()
                #         return self
                #     content_type = cgi.parse_header(
                #         response.headers.get("Content-Type", "")
                #     )[0]
                #     soup = (
                #         BeautifulSoup(text, "html.parser")
                #         if content_type == "text/html"
                #         else None
                #     )
        except RequestException as e:
            self.crawler.current_processed_count += 1
            processor = Error(self, e)
        else:
            await processor.process(self)
        finally:
            self.crawler.domain_semaphore.release(self.crawler_url.url.domain)
        return processor

    @property
    def soup(self):
        if self._soup is None and self.content is not None:
            self._soup = BeautifulSoup(self.content, "html.parser")
        return self._soup

    def __repr__(self):
        return "<CrawlerUrlRequest {}>".format(self.crawler_url.url)


class CrawlerUrl:
    processor: Optional["ProcessBase"] = None

    def __init__(
        self,
        crawler: "Crawler",
        target_url: str,
        depth=3,
        source=None,
        exists=None,
        url_type=None,
    ):
        """

        :type crawler: Crawler instance
        :type target_url: Uniform Resource Identifier as string
        :type depth: int maximum depth to crawl respect to the initial url
        """
        self.target_url = target_url
        url = Url(target_url)
        self.flags = set()
        self.depth = depth
        if url.is_valid():
            url.query = ""
            url.fragment = ""
        self.url = url
        self.crawler = crawler
        self.source = source
        self.exists = exists
        self.url_type = url_type
        if url.is_valid() and (not url.path or url.path == "/"):
            self.url_type = "directory"
        self.resp = None
        self.processor_data = None

    async def add_self_directories(self, exists=None, url_type=None):
        for url in self.url.breadcrumb():
            await self.crawler.add_crawler_url(
                CrawlerUrl(
                    self.crawler,
                    url,
                    self.depth - 1,
                    self,
                    exists,
                    url_type,
                )
            )
            # TODO: if exists=True and the urls is already processed before add it, but the already processed
            # url has exists=False, then update the exists to True

    async def retrieve(self):
        from processors import GenericProcessor

        crawler_url_request = CrawlerUrlRequest(self)
        processor = await crawler_url_request.retrieve()
        if processor is not None and not isinstance(processor, GenericProcessor):
            self.crawler.console.print(processor.get_text())
        # if self.must_be_downloaded(response):
        #     processor = get_processor(response, text, self, soup) or GenericProcessor(
        #         response, self
        #     )
        #     processor.process(text, soup)
        #     self.flags.update(processor.flags)
        # if self.maybe_directory():
        #     self.crawler.results.put(processor)
        # if processor is not None:
        #     self.processor_data = processor.json()
        # if processor and isinstance(processor, ProcessIndexOfRequest):
        #     self.crawler.index_of_processors.append(processor)
        # else:
        #     self.crawler.current_processed_count += 1
        if (
            self.exists is None
            and crawler_url_request.response is not None
            and crawler_url_request.response.status < 404
        ):
            self.exists = True
        # TODO: uncomment
        # await self.add_self_directories(
        #     True if (not self.maybe_rewrite() and self.exists) else None,
        #     "directory" if not self.maybe_rewrite() else None,
        # )

    def set_type(self, content_type):
        from dirhunt.processors import INDEX_FILES

        if not self.url_type and not (content_type or "").startswith("text/html"):
            self.url_type = "asset"
        if (
            not self.url_type
            and (content_type or "").startswith("text/html")
            and self.url.name in INDEX_FILES
        ):
            self.url_type = "document"

    def maybe_rewrite(self):
        return self.url_type not in ["asset", "directory"]

    def must_be_downloaded(self, response):
        """The file must be downloaded to obtain information."""
        return self.maybe_directory() or (
            cgi.parse_header(response.headers.get("Content-Type", ""))[0]
            in ["text/css", "application/javascript"]
        )

    def maybe_directory(self):
        return self.type not in ["asset", "document", "rewrite"] or self.type in [
            "directory"
        ]

    def result(self):
        # Cuando se ejecuta el result() de future, si ya está processed, devolverse a sí mismo
        return self

    def weight(self):
        value = sum([FLAGS_WEIGHT.get(flag, 0) for flag in self.flags])
        if self.url and self.url.is_valid():
            value -= len(list(self.url.breadcrumb())) * 1.5
        return value

    def json(self):
        return {
            "flags": self.flags,
            "depth": self.depth,
            "url": self.url,
            "type": self.type,
            "exists": self.exists,
        }

    def __repr__(self):
        return f"<CrawlerUrl {self.url}>"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CrawlerUrl):
            return False
        return self.url.url == other.url.url

    def __hash__(self):
        return hash(self.url.url)
