# encoding: utf-8
from z3c.form import field
from zope import schema
from zope.interface import implements
from zope.component import getUtility

from Acquisition import aq_inner, aq_parent
from AccessControl import getSecurityManager
from Products.CMFCore import permissions

from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.app.portlets.browser import z3cformhelper

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.interfaces import IPloneSiteRoot
import five.intid

from collective.person import MessageFactory as _


class IPersonPortlet(IPortletDataProvider):
    """
    """
    person_role = schema.TextLine(
        title=_(u"Role"),
        required=True,
        default=_(u"Shown as portlet title"),
        )


class Assignment(base.Assignment):
    """
    """

    implements(IPersonPortlet)

    person_role = u""

    def __init__(self, person_role, definition_context_id=None):
        self.person_role = person_role
        self.definition_context_id = definition_context_id

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u"Person portlet")


class Renderer(base.Renderer):
    """
    """

    render = ViewPageTemplateFile('personportlet.pt')

    def get_definition_context(self):
        site = getUtility(IPloneSiteRoot)
        intid = five.intid.site.get_intids(site)
        try:
            return intid.getObject(int(self.data.definition_context_id))
        except ValueError:
            pass  # not a reference

    @property
    def title(self):
        return self.data.person_role

    @property
    @memoize
    def contact_obj(self):
        """ get the contact object referenced from the project"""
        # TODO: what is goin to be shown? Selection? What if there is more than one?
        # other fields?
        try:
             internal_contacts = self.get_definition_context().internal_contacts
             if internal_contacts:
                 reference = internal_contacts[0]
                 obj = reference.to_object
                 if obj:
                     if getSecurityManager().checkPermission(permissions.View, obj) \
                       and not obj.isExpired():
                        return {'name': obj.Title(),
                                'url': obj.absolute_url(),
                                'empl_name': obj.getName(),
                                'empl_stillingsbetegnelse': obj.getStillingsbetegnelse(),
                                'empl_phone': obj.getPhone(),
                                'empl_email': obj.getEmail(),
                                'empl_portrait_url': obj.getImageUrl(),}

        except (AttributeError, IndexError):
            return None


#    @property
#    def job_title(self):
#        contact_obj = self.contact_obj()
#        if contact_obj:
#            if contact_obj.Language() == 'en':
#                return contact_obj.getJobTitleEn()
#            else:
#                return contact_obj.getJobTitle()
#        else:
#            return "No contact"

#    @property
#    def group_url(self):
#        # TODO: implement this when the lists of group members are ready
#        if self.data.show_group:
#            return 'abc'
#        else:
#            return ''

#    @property
#    def email(self):
#        contact_obj = self.contact_obj()
#        if contact_obj:
#            return contact_obj.getEmail()
#        else:
#            return "No contact"
#
#    @property
#    def phone(self):
#        contact_obj = self.contact_obj()
#        if contact_obj:
#            return contact_obj.getPhoneNumber()
#        else:
#            return "No contact"
#
#    @property
#    def photo(self):
#        contact_obj = self.contact_obj()
#        if contact_obj:
#            return contact_obj.getMyImage()
#        else:
#            return None


    @property
    @memoize
    def image_tag(self):
        return None
        #image.tag(scale='person_profile', css_class='imageItem personBoxImage', alt=view.name)

    @property
    def available(self):
        """Only make this available if a contact is referenced from the project.
        """
        return self.contact_obj

class AddForm(z3cformhelper.AddForm):
    """
    """
    fields = field.Fields(IPersonPortlet)

    label = _(u"Add Person Portlet")
    description = _(u"description_add_portlet", default=u"This portlet display info about the person"
                                                         "referenced from the content item where the portlet is created.")

    def create_assignment(self, data):
        site = getUtility(IPloneSiteRoot)
        intid = five.intid.site.get_intids(site)
        # first strip the aq wrapper, then get the parent =  PortletAssignmentMapping,
        # and then the parent of that = definition context = the plone content object where the portlet is added.
        definition_context = aq_parent(aq_parent(aq_inner(self.context)))
        definition_context_id = intid.getId(definition_context)

        return Assignment(definition_context_id = definition_context_id, **data)


class EditForm(z3cformhelper.EditForm):
    """
    """
    fields = field.Fields(IPersonPortlet)

    label = _(u"Edit Person Portlet")
    description = _(u"description_add_portlet", default=u"This portlet display info about the person"
                                                         "referenced from the content item where the portlet is created.")

