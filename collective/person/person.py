# -*- coding: utf-8 -*-
from zope.interface import Interface, implements
from plone.dexterity.content import Item
from plone.app.imagecropping.interfaces import IImageCropping

class IPerson(Interface, IImageCropping):
    """ Publication """

class Person(Item):
    """Customised person content class"""
    implements(IPerson)

    @property
    def title(self):
        names = [
            self.firstname,
            self.lastname,
        ]
        return u' '.join([name for name in names if name])

    def setTitle(self, value):
        return
