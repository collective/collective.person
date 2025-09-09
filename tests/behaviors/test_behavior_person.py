from collective.person.behaviors.person import IPersonData
from collective.person.behaviors.person import IPersonDataMarker
from copy import deepcopy
from plone import api

import pytest


TYPE = "Person"


@pytest.fixture
def portal(integration, get_fti):
    fti = get_fti(TYPE)
    current = list(fti.behaviors)
    behaviors = current[:]
    fti.behaviors = tuple(behaviors)
    yield integration["portal"]
    fti.behaviors = tuple(current)


@pytest.fixture
def person(persons_payload, portal):
    payload = deepcopy(persons_payload[0])
    with api.env.adopt_roles(["Manager", "Member"]):
        content = api.content.create(container=portal, **payload)
    return content


@pytest.fixture
def other_person(persons_payload, portal, user):
    payload = deepcopy(persons_payload[1])
    with api.env.adopt_roles(["Manager", "Member"]):
        content = api.content.create(container=portal, **payload)
    return content


class TestPersonDataBehavior:
    BEHAVIOR = "collective.person.person"

    @pytest.fixture(autouse=True)
    def _init(self, portal, person):
        self.portal = portal
        self.person = person

    def test_behavior_enabled(self, get_behaviors):
        """Test if behavior is installed for Person."""
        assert self.BEHAVIOR in get_behaviors(TYPE)

    def test_behavior_marker_is_provided(self):
        """Test if behavior is provided by a Person instance."""
        content = self.person
        assert IPersonDataMarker.providedBy(content)

    def test_title_result(self):
        """Test content title."""
        content = self.person
        assert content.title == "Douglas Adams"

    def test_indexer_sortable_title(self):
        """Test title indexer."""
        content = self.person
        brains = api.content.find(sortable_title="douglas adams")
        assert len(brains) == 1
        assert content.UID() == brains[0].UID

    def test_indexer_searchable_text(self):
        """Test searchable text indexer."""
        content = self.person
        brains = api.content.find(SearchableText="writer")
        assert len(brains) == 1
        assert content.UID() == brains[0].UID

    def test_indexer_title(self):
        """Test title indexer."""
        content = self.person
        title = IPersonData(content).title
        brains = api.content.find(Title=title)
        assert len(brains) == 1
        assert brains[0].Title == title

    def test_indexer_roles(self):
        content = self.person
        brains = api.content.find(roles="member")
        assert len(brains) == 1
        assert content.UID() == brains[0].UID
