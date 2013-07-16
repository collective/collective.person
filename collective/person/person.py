# -*- coding: utf-8 -*-
from zope import schema

from plone.directives import form
from plone.dexterity.content import Item
from collective import dexteritytextindexer
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from plone.app.imagecropping.interfaces import IImageCropping

from Products.CMFPlone import PloneMessageFactory as _pmf
from collective.person import MessageFactory as _

class IMinimalPerson(form.Schema):
    """ Minimal """

    dexteritytextindexer.searchable('firstname')
    firstname = schema.TextLine(
        title=_(u"First name"),
        required=True,
    )

    dexteritytextindexer.searchable('lastname')
    lastname = schema.TextLine(
        title=_(u"Last name"),
        required=True,
    )


class IPerson(IMinimalPerson, IImageCropping):
    """ Represents an Person.
        Displayed in a contacts portlet.
        """

    dexteritytextindexer.searchable('email')
    email = schema.TextLine(
        title=_(u"Email"),
        required=False,
    )

    dexteritytextindexer.searchable('phone')
    phone = schema.TextLine(
        title=_(u"Phone"),
        required=False,
    )

    dexteritytextindexer.searchable('jobtitle')
    jobtitle = schema.TextLine(
        title=_(u"Danish Job title"),
        required=False,
    )

    image = NamedBlobImage(
        title=_(u"Portrait"),
        required=False
    )

    dexteritytextindexer.searchable('text')
    text = RichText(
        title=_(u"Text"),
        required=False,
    )


class Person(Item):
    """Customised person content class"""

    @property
    def title(self):
        names = [
            self.firstname,
            self.lastname,
        ]
        return u' '.join([name for name in names if name])

    def setTitle(self, value):
        return
