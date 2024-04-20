$ dirhunt https://victim.victim.victim/ --exclude-sources certificatessl --threads 40 >test
$ cat test
200: https://victim.victim.victim/.well-known/assetlinks.json
200: https://victim.victim.victim/.well-known/gpc.json
404: https://victim.victim.victim/.well-known/nodeinfo
ERR: https://victim.victim.victim/static/front/fonts/bodonimoda-600-italic.862fa920.ttf
ERR: https://victim.victim.victim/static/front/fonts/bodonimoda-500-normal.c152933f.ttf
500: https://victim.victim.victim/static/front/fonts/bodonimoda-800-italic.c4f1cf28.ttf
200: https://victim.victim.victim/static/front/fonts/bodonimoda-700-italic.85b9582e.ttf
200: https://victim.victim.victim/static/front/fonts/bodonimoda-900-italic.76fe8150.ttf
ERR: https://victim.victim.victim/static/front/fonts/bodonimoda-900-normal.d46f53e1.ttf
ERR: https://victim.victim.victim/static/front/fonts/cutivemono-400-normal.49663c3e.ttf

.. image:: https://raw.githubusercontent.com/Nekmo/dirhunt/v0.2.0/images/dirhunt.png

|

.. image:: https://raw.githubusercontent.com/Nekmo/dirhunt/pip-rating-badge/pip-rating-badge.svg
  :target: https://github.com/Nekmo/dirhunt/actions/workflows/pip-rating.yml
  :alt: pip-rating badge

.. image:: https://img.shields.io/github/actions/workflow/status/Nekmo/dirhunt/test.yml?style=flat-square&maxAge=2592000&branch=develop
  :target: https://github.com/Nekmo/dirhunt/actions?query=workflow%3ATests
  :alt: Latest Tests CI build status

.. image:: https://img.shields.io/pypi/v/dirhunt.svg?style=flat-square
  :target: https://pypi.org/project/dirhunt/
  :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/pyversions/dirhunt.svg?style=flat-square
  :target: https://pypi.org/project/dirhunt/
  :alt: Python versions

.. image:: https://img.shields.io/codeclimate/maintainability/Nekmo/dirhunt.svg?style=flat-square
  :target: https://codeclimate.com/github/Nekmo/dirhunt
  :alt: Code Climate

.. image:: https://img.shields.io/codecov/c/github/Nekmo/dirhunt/master.svg?style=flat-square
  :target: https://codecov.io/github/Nekmo/dirhunt
  :alt: Test coverage

.. image:: https://img.shields.io/github/stars/Nekmo/dirhunt?style=flat-square
     :target: https://github.com/Nekmo/dirhunt
     :alt: Github stars


Dirhunt
#######

.. image:: https://asciinema.org/a/xPJXT0MhrvlZ8lJYJYkjxlice.png
     :target: https://asciinema.org/a/xPJXT0MhrvlZ8lJYJYkjxlice
     :align: center
     :alt: Dirhunt Demo Video


Dirhunt is a web crawler optimize for **search and analyze directories**. This tool can find interesting things if the
server has the *"index of"* mode enabled. Dirhunt is also useful if the directory listing is not enabled. It detects
directories with **false 404 errors**, directories where an **empty index file** has been created to hide things and
much more.

.. code-block:: console

    $ dirhunt http://website.com/

Dirhunt does not use brute force. But neither is it just a **crawler**. This tool is faster than others because it
minimizes requests to the server. Generally, this tool takes **between 5-30 seconds**, depending on the website and
the server.

Read more about **how to use** Dirhunt `in the documentation <http://docs.nekmo.org/dirhunt/usage.html>`_.


Features
========

* Process **one or multiple sites** at a time.
* Process *'Index Of'* pages and report interesting files.
* Detect **redirectors**.
* Detect **blank index file** created on directory to hide things.
* Process some html files in search of new directories.
* 404 error pages and detect **fake 404 errors**.
* Filter results by **flags**.
* Analyze results at end. It also **processes date & size** of the Index Pages.
* Get new directories using **robots.txt**, **VirusTotal**, **Google**, **CommonCrawl** (NEW!),
  **SSL Certificate** (NEW!), **Crt.sh** (NEW!) & **Wayback** (NEW!).
* **Delay** between requests.
* One or multiple **proxies** option. It can also search for **free proxies**.
* **Save the results** to a JSON file
* **Resume** the aborted scans


Install
=======
If you have Pip installed on your system, you can use it to install the latest Dirhunt stable version::

    $ sudo pip3 install dirhunt

Python 2.7 & 3.7-3.12 are supported but Python 3.x is recommended. Use ``pip2`` on install for Python2.

There are other `installation methods <http://docs.nekmo.org/dirhunt/installation.html>`_ available.


Disclaimer
==========
This software must not be used on third-party servers without permission. Dirhunt has been created to be used by audit
teams with the consent of the owners of the website analyzed. The author is not responsible for the use of this tool
outside the law.

This software is under the MIT license. The author does not provide any warranty. But issues and pull requests are
welcome.
