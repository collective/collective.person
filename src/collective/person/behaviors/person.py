from collective.person import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IPersonData(model.Schema):
    """A Person."""

    title = schema.TextLine(readonly=True)

    first_name = schema.TextLine(
        title=_("label_first_name", default="First Name"),
        description=_("help_first_name", default="First name of this person."),
        required=True,
    )

    last_name = schema.TextLine(
        title=_("label_last_name", default="Last Name"),
        description=_("help_last_name", default="Last Name of this person."),
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
