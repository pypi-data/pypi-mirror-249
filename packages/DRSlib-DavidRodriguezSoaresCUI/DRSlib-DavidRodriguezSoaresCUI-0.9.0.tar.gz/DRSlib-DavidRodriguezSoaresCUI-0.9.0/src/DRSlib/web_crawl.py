"""
web crawler library
===================

Contains a few nice-to-haves as far as web crawling goes; still in early development
"""

import urllib3


PM = urllib3.PoolManager()


def get_html(url: str) -> str:
    """Get HTML content from URL"""
    response: urllib3.response.HTTPResponse = PM.request("GET", url)
    if response.status == 200:
        return response.data.decode(encoding="utf8")
    raise ValueError(f"Return status is {response.status}")


def get_img(url: str) -> bytes:
    """Get image content from URL"""
    response: urllib3.response.HTTPResponse = PM.request("GET", url)
    if response.status == 200:
        return response.data
    raise ValueError(f"Return status is {response.status}")
