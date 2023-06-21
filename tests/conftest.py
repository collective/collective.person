from collective.person.testing import FUNCTIONAL_TESTING
from collective.person.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import SITE_OWNER_NAME
from pytest_plone import fixtures_factory

import pytest


pytest_plugins = ["pytest_plone"]


globals().update(
    fixtures_factory(
        (
            (FUNCTIONAL_TESTING, "functional"),
            (INTEGRATION_TESTING, "integration"),
        )
    )
)


@pytest.fixture()
def roles_vocab():
    return {
        "items": [
            {
                "token": "member",
                "titles": {
                    "en": "Team Member",
                },
            },
            {
                "token": "student",
                "titles": {
                    "en": "Student",
                },
            },
        ]
    }


@pytest.fixture()
def portal(integration, roles_vocab):
    portal = integration["portal"]
    with api.env.adopt_user(SITE_OWNER_NAME):
        # Set registry for roles
        api.portal.set_registry_record("person.roles", roles_vocab)
    return portal


@pytest.fixture
def persons_payload() -> list:
    """Payload to create two persons items."""
    return [
        {
            "type": "Person",
            "id": "douglas-adams",
            "first_name": "Douglas",
            "last_name": "Adams",
            "description": "A very good writer",
            "roles": ["member"],
        },
        {
            "type": "Person",
            "id": "marvin",
            "first_name": "Marvin",
            "last_name": "",
            "description": "A very good nice robot",
            "roles": ["member"],
        },
    ]


@pytest.fixture
def persons(portal, persons_payload) -> dict:
    """Create Person content items."""
    response = {}
    with api.env.adopt_roles(
        [
            "Manager",
        ]
    ):
        for data in persons_payload:
            content = api.content.create(container=portal, **data)
            response[content.UID()] = content.title
    return response


@pytest.fixture
def person(persons) -> dict:
    """Return one Person."""
    content_uid = [key for key in persons.keys()][0]
    brains = api.content.find(UID=content_uid)
    return brains[0].getObject()
