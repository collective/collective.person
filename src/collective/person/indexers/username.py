from collective.person.behaviors.user import IPloneUser
from collective.person.behaviors.user import IPloneUserMarker
from plone.indexer import indexer


@indexer(IPloneUserMarker)
def username(obj):
    return IPloneUser(obj).username
