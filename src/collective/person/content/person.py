from plone.dexterity.content import Container
from zope.interface import implementer
from zope.interface import Interface


class IPerson(Interface):
    """A Person."""


@implementer(IPerson)
class Person(Container):
    """A Person."""

    @property
    def title(self) -> str:
        """Create title by joining name fields."""
        # Fallback implementing the old logic to return the title
        from collective.person.behaviors.person import IPersonData

        behavior = IPersonData(self)
        return behavior.title

    @title.setter
    def title(self, value: str):
        # title is not writable
        pass
