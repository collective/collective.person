from plone.dexterity.fti import DexterityFTI
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility

import pytest


@pytest.fixture(scope="class")
def get_fti(portal_class):
    def get_fti(name: str) -> DexterityFTI:
        """Get the Factory Type Information for a type by name."""
        return queryUtility(IDexterityFTI, name=name)

    return get_fti
