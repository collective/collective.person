from collective.person import _
from collective.person.content.person import Person
from collective.person.interfaces import IPersonTitle
from collective.person.interfaces import PersonTitle
from plone import api
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider


def get_title_utility() -> PersonTitle:
    """Return the title utility to be used to generate titles."""
    utility_name = api.portal.get_registry_record(
        "person.title_utility", default="first_last"
    )
    utility: PersonTitle = getUtility(IPersonTitle, name=utility_name)
    return utility


class IPersonDataMarker(Interface):
    """Marker interface for content types or instances that implement the
    behavior collective.person.person."""


@provider(IFormFieldProvider)
class IPersonData(model.Schema):
    """A Person."""

    title = schema.TextLine(readonly=True)

    first_name = schema.TextLine(
        title=_("label_first_name", default="First Name"),
        required=True,
    )

    last_name = schema.TextLine(
        title=_("label_last_name", default="Last Name"),
        required=False,
    )

    description = schema.Text(
        title=_("label_person_description", default="Bio"),
        description=_(
            "help_person_description", default="A short biography for this person."
        ),
        required=False,
    )

    roles = schema.List(
        title=_("label_person_roles", default="Roles"),
        description=_("help_person_roles", default="Roles for this person."),
        default=[],
        value_type=schema.Choice(
            vocabulary="collective.person.available_roles",
        ),
        required=False,
    )


@implementer(IPersonData)
@adapter(IPersonDataMarker)
class PersonData:
    """Adapter for person data behavior."""

    def __init__(self, context: Person):
        self.context = context

    @property
    def title(self) -> str:
        """Create title by joining name fields."""
        utility = get_title_utility()
        context = self.context
        return utility.title(context)

    @title.setter
    def title(self, value: str):
        """We do not support setting the title directly."""
        pass

    @property
    def first_name(self) -> str:
        """Return the first name."""
        return self.context.first_name

    @first_name.setter
    def first_name(self, value: str):
        """Set first_name attribute on the object."""
        self.context.first_name = value

    @property
    def last_name(self) -> str:
        """Return the last name."""
        return self.context.last_name

    @last_name.setter
    def last_name(self, value: str):
        """Set last_name attribute on the object."""
        self.context.last_name = value

    @property
    def description(self) -> str:
        """Return the description."""
        return self.context.description

    @description.setter
    def description(self, value: str):
        """Set description attribute on the object."""
        self.context.description = value

    @property
    def roles(self) -> list[str]:
        """Return the roles."""
        return self.context.roles

    @roles.setter
    def roles(self, value: list[str]):
        """Set roles attribute on the object."""
        self.context.roles = value
