from collective.person.content.person import Person
from plone import api

import pytest


@pytest.fixture
def payload(persons_payload: list[dict]) -> dict:
    """Return the first person payload."""
    return persons_payload[0]


@pytest.fixture
def person(portal, payload: dict) -> Person:
    """Create a Person content item."""
    with api.env.adopt_roles(["Manager"]):
        content = api.content.create(container=portal, **payload)
    return content


class TitleUtility:
    """Test title utilities."""

    utility_name: str = "default"

    @pytest.fixture(autouse=True)
    def _setup(self, portal):
        self.portal = portal
        api.portal.set_registry_record("person.title_utility", self.utility_name)


class TestTitleUtilityDefault(TitleUtility):
    utility_name: str = "first_last"

    def test_title(self, person):
        """Test that titles are generated correctly using the default utility."""
        first_name = person.first_name
        last_name = person.last_name
        expected = f"{first_name} {last_name}".strip()
        assert person.title == expected

    def test_brain(self, person):
        """Test titles are correctly indexed."""
        uid = api.content.get_uuid(person)
        first_name = person.first_name
        last_name = person.last_name
        expected = f"{first_name} {last_name}".strip()
        brains = api.content.find(UID=uid)
        assert len(brains) == 1
        assert brains[0].Title == expected


class TestTitleUtilityLastFirst(TitleUtility):
    utility_name: str = "last_first"

    def test_title(self, person):
        """Test that titles are generated correctly using the default utility."""
        first_name = person.first_name
        last_name = person.last_name
        expected = f"{last_name}, {first_name}".strip()
        assert person.title == expected

    def test_brain(self, person):
        """Test titles are correctly indexed."""
        uid = api.content.get_uuid(person)
        first_name = person.first_name
        last_name = person.last_name
        expected = f"{last_name}, {first_name}".strip()
        brains = api.content.find(UID=uid)
        assert len(brains) == 1
        assert brains[0].Title == expected
