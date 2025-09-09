"""Module where all interfaces, events and exceptions live."""

from typing import Protocol
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IPersonLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IPersonTitle(Interface):
    """Implement a title utility for person objects."""

    name: str

    def title(self, context) -> str:
        """Return the title of the person."""


class PersonTitle(Protocol):
    """Implement a title utility for person objects."""

    name: str

    def title(self, context) -> str:
        """Return the title of the person."""
