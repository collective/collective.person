from collective.person import _
from collective.person.content.person import Person
from collective.person.interfaces import IPersonTitle
from zope.interface import implementer


@implementer(IPersonTitle)
class FirstLastName:
    """Return the title with 'first_name last_name'."""

    name: str = _("First and Last Name")

    def title(self, context: Person) -> str:
        """Return the title of the person."""
        first_name = context.first_name
        last_name = context.last_name or ""
        return f"{first_name} {last_name}".strip()


@implementer(IPersonTitle)
class LastFirstName:
    """Return the title with 'last_name, first_name'."""

    name: str = _("Last and First Name")

    def title(self, context: Person) -> str:
        """Return the title of the person."""
        first_name = context.first_name
        last_name = context.last_name or ""
        title = f"{last_name}, {first_name}" if last_name else first_name
        return title.strip()
