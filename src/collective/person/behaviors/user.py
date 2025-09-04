from collective.person import _
from plone import api
from plone.app.content.interfaces import INameFromTitle
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import Invalid
from zope.interface import invariant
from zope.interface import provider


ANNO_KEY = "collective.person.username"


def validate_username(username: str):
    """Check if a username is a valid one and not in use."""
    user = api.user.get(username=username)
    if not user:
        return _("There is no user with this username")

    results = api.content.find(username=username)
    if len(results) > 0:
        return _("There is a person already assigned to this username")


class IPloneUserMarker(Interface):
    """Marker interface for content types or instances that are connected to a user."""


@provider(IFormFieldProvider)
class IPloneUser(model.Schema):
    """Behavior for integration between a dexterity type and a Plone user."""

    username = schema.Choice(
        title=_("Username"),
        description=_("Please inform a username to be used."),
        vocabulary="plone.app.vocabularies.Users",
        default="",
        required=False,
    )

    @invariant
    def username_unique(data):
        """Username must be unique on the site."""
        context = getattr(data, "__context__", None)
        username = getattr(data, "username", None)
        if not username:
            return
        if context is not None and IPloneUser(context).username == username:
            # No change, fine.
            return
        error = validate_username(username)
        if error:
            raise Invalid(error)


@implementer(IPloneUser)
@adapter(IPloneUserMarker)
class PloneUser:
    """Adapter for plone user behavior."""

    def __init__(self, context):
        self.context = context
        self.annotation = IAnnotations(context)

    @property
    def username(self):
        return self.annotation.get(ANNO_KEY, "")

    @username.setter
    def username(self, value):
        current = self.username
        if value == current:
            return
        error = validate_username(value)
        if not error:
            self.annotation[ANNO_KEY] = value
        else:
            raise Invalid(error)

    @property
    def user(self):
        """Return the Plone User."""
        username = self.username
        if username:
            return api.user.get(username=username)
        return


class INameFromUserName(Interface):
    """Get the name from the user_name field value.

    This is really just a marker interface, automatically set by
    enabling the corresponding behavior.

    Note that when you want this behavior, then you MUST NOT enable
    INameFromTitle or INameFromFile behaviors
    on your type.
    """


@implementer(INameFromTitle)
@adapter(INameFromUserName)
class NameFromUserName:
    def __init__(self, context):
        self.context = context
        self.annotation = IAnnotations(self.context)

    @property
    def title(self):
        anno = self.annotation
        if anno and ANNO_KEY in anno:
            return anno[ANNO_KEY]
        else:
            return self.context.title
