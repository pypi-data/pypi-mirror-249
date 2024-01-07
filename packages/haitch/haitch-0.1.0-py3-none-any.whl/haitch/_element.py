from __future__ import annotations

import functools
import html
from typing import Iterable, Mapping, Union


class Element:
    """Lazily built HTML Element.

    An Element represents a Document Object Model (DOM) with optional
    attributes and children. Render the HTML to string by invoking the
    `__str__` method.
    """

    def __init__(self, tag: str) -> None:
        """Initialize element by providing a tag name, ie. "a", "div", etc."""
        self._tag = tag
        self._attrs: Mapping[str, AttributeValue] = {}
        self._children: Iterable[Child] = []

    def __call__(self, *children: Child, **attrs: AttributeValue) -> Element:
        """Add children and/or attributes to element.

        Provide attributes, children, or a combination of both:

        >>> import haitch as H
        >>> H.img(src="h.png", alt="Letter H")
        >>> H.h1("My heading")
        >>> H.h1(style="color: red;")("My heading")
        """
        if children:
            self._children = [*self._children, *children]

        if attrs:
            self._attrs = {**self._attrs, **attrs}

        return self

    @functools.cached_property
    def is_void(self) -> bool:
        """Check if element is considered a void element.

        https://developer.mozilla.org/en-US/docs/Glossary/Void_element
        """
        return self._tag in {
            "area",
            "base",
            "br",
            "col",
            "embed",
            "hr",
            "img",
            "input",
            "line",
            "link",
            "meta",
            "param",
            "source",
            "track",
            "wbr",
        }

    def __str__(self) -> str:
        """Renders the HTML element as a string."""
        return self._render()

    def _render(self) -> str:
        attrs_ = "".join(self._serialize_attr(k, v) for k, v in self._attrs.items())

        if self.is_void:
            return "<%(tag)s%(attrs)s/>" % {"tag": self._tag, "attrs": attrs_}

        children_ = "".join(self._render_child(child) for child in self._children)

        return "<%(tag)s%(attrs)s>%(children)s</%(tag)s>" % {
            "tag": self._tag,
            "attrs": attrs_,
            "children": children_,
        }

    def _render_child(self, child: Child) -> str:
        if isinstance(child, str):
            return html.escape(child)

        if isinstance(child, Element):
            return child._render()

        raise ValueError(f"Child must be `str` or `Element`, not {type(child)}")

    @staticmethod
    def _serialize_attr(key: str, value: AttributeValue) -> str:
        key_ = key.rstrip("_").replace("_", "-")

        if isinstance(value, bool):
            return " %(key)s" % {"key": key_} if value else ""

        if isinstance(value, str):
            value_ = html.escape(value)
            return ' %(key)s="%(value)s"' % {"key": key_, "value": value_}

        raise ValueError(f"Attribute value must be `str` or `bool`, not {type(value)}")


Child = Union[str, Element]
"""An acceptable child type to be passed to an element."""

AttributeValue = Union[str, bool]
"""An acceptable value type to be passed to an attribute."""
