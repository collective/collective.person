from collective.person.behaviors.user import INameFromUserName
from collective.person.behaviors.user import IPloneUser
from collective.person.behaviors.user import IPloneUserMarker
from copy import deepcopy
from dataclasses import dataclass
from plone import api
from Products.PlonePAS.tools.memberdata import MemberData
from typing import Any
from zope.interface import Invalid

import pytest


TYPE = "Person"


@dataclass()
class PloneUserData:
    context: Any
    username: str

    @property
    def __context__(self):
        return self.context


@pytest.fixture
def portal(integration, get_fti):
    fti = get_fti(TYPE)
    current = list(fti.behaviors)
    behaviors = current[:]
    # Remove plone.namefromtitle
    behaviors.remove("plone.namefromtitle")
    # Add local behaviors
    behaviors.append("collective.person.user")
    behaviors.append("collective.person.namefromusername")
    fti.behaviors = tuple(behaviors)
    yield integration["portal"]
    fti.behaviors = tuple(current)


@pytest.fixture
def user(portal):
    with api.env.adopt_roles(["Manager", "Member"]):
        user = api.user.create(
            email="adams@foo.bar",
            username="adams",
            password="averylongpasswordbutnotthatlong",  # noQA: S106
            roles=["Member"],
        )
    return user


@pytest.fixture
def person(persons_payload, portal, user):
    payload = deepcopy(persons_payload[0])
    with api.env.adopt_roles(["Manager", "Member"]):
        content = api.content.create(container=portal, **payload)
        IPloneUser(content).username = user.getUserName()
        content.reindexObject(idxs=["username"])
    return content


@pytest.fixture
def other_person(persons_payload, portal, user):
    payload = deepcopy(persons_payload[1])
    with api.env.adopt_roles(["Manager", "Member"]):
        content = api.content.create(container=portal, **payload)
    return content


class TestPloneUserBehavior:
    BEHAVIOR = "collective.person.user"

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
        assert IPloneUserMarker.providedBy(content)

    def test_behavior_user(self):
        """Test if behavior returns a valid user."""
        content = self.person
        behavior = IPloneUser(content)
        username = behavior.username
        assert isinstance(behavior.user, MemberData)
        assert behavior.user.getUserName() == username

    def test_indexer_username(self):
        """Test username indexer."""
        content = self.person
        username = IPloneUser(content).username
        brains = api.content.find(username=username)
        assert len(brains) == 1
        assert brains[0].username == username

    def test_username_validation_no_user(self):
        """Test username validation when user does not exist."""
        data = PloneUserData(context=self.person, username="nonexisting")

        with pytest.raises(Invalid) as exc:
            IPloneUser.validateInvariants(data)
        assert "There is no user with this username" in str(exc)

    def test_username_validation_invalid_username(self, other_person):
        """Test username validation when username is taken."""
        data = PloneUserData(context=other_person, username="adams")

        with pytest.raises(Invalid) as exc:
            IPloneUser.validateInvariants(data)
        assert "There is a person already assigned to this username" in str(exc)


class TestNameFromUserNameBehavior:
    BEHAVIOR = "collective.person.namefromusername"

    @pytest.fixture(autouse=True)
    def _init(self, portal, person):
        self.portal = portal
        self.person = person

    def test_behavior_enabled(self, get_behaviors):
        """Test if behavior is installed for Person."""
        assert self.BEHAVIOR in get_behaviors(TYPE)

    def test_adapt_content(self):
        """Test if behavior adapts content."""
        content = self.person
        assert INameFromUserName.providedBy(content)

    def test_provide_new_id(self):
        """Test behavior provides new it."""
        from plone.app.content.interfaces import INameFromTitle

        content = self.person
        username = IPloneUser(content).username
        assert INameFromTitle(content).title == username
