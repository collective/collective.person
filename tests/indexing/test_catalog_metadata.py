from collective.person.behaviors.person import IPersonDataMarker
from plone import api

import pytest


@pytest.mark.portal(
    profiles=[
        "collective.person:demo",
        "collective.person:catalog",
    ],
)
class TestCatalogMetadata:
    @pytest.fixture(autouse=True)
    def _setup(self, portal_class):
        self.portal = portal_class

    @pytest.mark.parametrize(
        "query,column,expected",
        [
            (
                {"portal_type": "Person", "Title": "Elnor"},
                "contact_email",
                "elnor@starfleet.space",
            ),
            ({"portal_type": "Person", "Title": "Elnor"}, "contact_phone", None),
            (
                {"portal_type": "Person", "Title": "Elnor"},
                "contact_website",
                "https://starfleet.space",
            ),
            (
                {"object_provides": IPersonDataMarker, "Title": "Ortegas"},
                "contact_email",
                "ortegas@starfleet.space",
            ),
            (
                {"object_provides": IPersonDataMarker, "Title": "Ortegas"},
                "contact_phone",
                "+99325421255",
            ),
            (
                {"object_provides": IPersonDataMarker, "Title": "Ortegas"},
                "contact_website",
                "https://starfleet.space",
            ),
        ],
    )
    def test_additional_metadata(self, query: dict, column: str, expected: str | None):
        """Test title indexer."""
        brains = api.content.find(**query)
        assert len(brains) == 1
        assert getattr(brains[0], column) == expected
