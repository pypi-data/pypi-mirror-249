"""
haitch - a lazy HTML element builder.
=====================================

Import any element you like from the root module:

>>> import haitch as H

Lazily build a dom tree by passing children and/or attributes to the
`__init__` and/or `__call__` methods:

>>> dom = H.a(href="https://example.com")("Check out my website")

In order render the object to HTML, you need to invoke the `__str__` method:

>>> str(dom)
'<a href="https://example.com">Check out my website</a>'
"""

from haitch._element import Element

__all__ = ["Element"]


def __getattr__(tag: str) -> Element:
    return Element(tag)
