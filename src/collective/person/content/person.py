from plone.dexterity.content import Container
from zope.interface import implementer
from zope.interface import Interface


class IPerson(Interface):
    """A Person."""


@implementer(IPerson)
class Person(Container):
    """A Person."""

    @property
    def title(self):
        """Create title by joining name fields."""
        first_name = self.first_name
        last_name = self.last_name or ""
        return f"{first_name} {last_name}".strip()

    @title.setter
    def title(self, value):
        # title is not writable
        pass
