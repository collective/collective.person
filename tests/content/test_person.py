from collective.person.content.person import Person
from plone import api
from plone.dexterity.fti import DexterityFTI
from zope.component import createObject

import pytest


CONTENT_TYPE = "Person"


class TestPersonFTI:
    @pytest.fixture(autouse=True)
    def _setup(self, get_fti):
        self.fti = get_fti(CONTENT_TYPE)

    def test_factory(self):
        factory = self.fti.factory
        obj = createObject(factory)
        assert obj is not None
        assert isinstance(obj, Person)

    @pytest.mark.parametrize(
        "attr,expected",
        [
            ("title", "Person"),
            ("description", ""),
            ("global_allow", True),
            ("filter_content_types", True),
            (
                "allowed_content_types",
                (
                    "File",
                    "Image",
                ),
            ),
            ("add_permission", "collective.person.person.add"),
            ("klass", "collective.person.content.person.Person"),
            (
                "behaviors",
                (
                    "collective.person.person",
                    "collective.contact_behaviors.contact_info",
                    "volto.blocks.editable.layout",
                    "plone.namefromtitle",
                    "plone.shortname",
                    "plone.leadimage",
                    "plone.excludefromnavigation",
                    "plone.relateditems",
                    "plone.versioning",
                ),
            ),
        ],
    )
    def test_fti(self, attr: str, expected):
        """Test FTI values."""
        fti: DexterityFTI = self.fti

        assert isinstance(fti, DexterityFTI)
        assert getattr(fti, attr) == expected


class TestPerson:
    @pytest.fixture(autouse=True)
    def _setup(self, portal):
        self.portal = portal

    def test_create(self, portal, persons_payload):
        payload = persons_payload[0]
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=portal, **payload)
        assert content.portal_type == CONTENT_TYPE
        assert isinstance(content, Person)
        assert content.title == "Douglas Adams"
