# encoding: utf-8
from z3c.form import field
from zope import schema
from zope.interface import implements

from AccessControl import getSecurityManager
from Products.CMFCore import permissions

from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from plone.app.portlets.portlets import base
from plone.app.portlets.browser import z3cformhelper

from plone.formwidget.contenttree import ObjPathSourceBinder
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.interfaces import IHasOutgoingRelations

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.person.person import IPerson

from collective.person import MessageFactory as _


class IPersonReferencePortlet(IPortletDataProvider):
    """
    """

    header = schema.TextLine(
        title=_(u"Portlet header"),
        default=_(u"Title of the rendered portlet."
                   " Could be a role of the person in the context of the portlet."),
        required=True,
        )

    person = RelationChoice(
        title=_(u"Person"),
        description=_(u"description_target", default=u"Find object for reference"),
        required=True,
        source=ObjPathSourceBinder(object_provides=IPerson.__identifier__),
        )


class Assignment(base.Assignment):
    """
    """

    implements(IPersonReferencePortlet, IHasOutgoingRelations)

    header = u""
    person = None

    def __init__(self, header, person=None):
        self.header = header
        self.person = person

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        if self.header:
            return self.header + ': ' + _(u"Person reference portlet")
        return _(u"Person reference portlet")


class Renderer(base.Renderer):
    """
    """

    render = ViewPageTemplateFile('personportlet.pt')

    @property
    def title(self):
        return self.data.header

    @property
    @memoize
    def person(self):
        """ get the object the portlet is pointing to """
        if self.data.person is not None:
            obj = self.data.person.to_object
            if obj:
                if getSecurityManager().checkPermission(permissions.View, obj) \
                  and not obj.isExpired():
                    return obj

    @property
    def available(self):
        """Only make this available if a person is referenced from the project.
        """
        return self.person is not None

class AddForm(z3cformhelper.AddForm):
    """
    """
    fields = field.Fields(IPersonReferencePortlet)

    label = _(u"Add Person Reference Portlet")
    description = _(u"description_add_ref_portlet",
                    default=u"This portlet display info about the person "
                             "referenced from the portlet.")

    def create(self, data):
        return Assignment(**data)


class EditForm(z3cformhelper.EditForm):
    """
    """
    fields = field.Fields(IPersonReferencePortlet)

    label = _(u"Edit Person Reference Portlet")
    description = _(u"description_add_portlet",
                    default=u"This portlet display info about the person "
                             "referenced from the portlet.")
