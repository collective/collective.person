from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.restapi.testing import RelativeSession

import pytest
import transaction


@pytest.fixture()
def roles_vocab():
    return {
        "items": [
            {
                "token": "member",
                "titles": {
                    "en": "Team Member",
                    "pt-br": "Colaborador",
                },
            },
            {
                "token": "student",
                "titles": {
                    "en": "Student",
                    "pt-br": "Estudante",
                },
            },
        ]
    }


def _create_content(portal, payload):
    """Create a content in the root of the portal."""
    return api.content.create(container=portal, **payload)


def _publish_content(content):
    """Publish a content."""
    api.content.transition(content, transition="publish")


@pytest.fixture()
def app(functional):
    return functional["app"]


@pytest.fixture()
def portal(functional, persons_payload, roles_vocab):
    portal = functional["portal"]
    with api.env.adopt_user(SITE_OWNER_NAME):
        # Set registry for roles
        api.portal.set_registry_record("person.roles", roles_vocab)
        # Create Content
        content = _create_content(portal, persons_payload[0])
    with api.env.adopt_user(SITE_OWNER_NAME):
        # Publish Content
        _publish_content(content)

    transaction.commit()
    return portal


@pytest.fixture()
def http_request(functional):
    return functional["request"]


@pytest.fixture()
def request_factory(portal):
    def factory():
        url = portal.absolute_url()
        api_session = RelativeSession(url)
        api_session.headers.update({"Accept": "application/json"})
        return api_session

    return factory


@pytest.fixture()
def anon_request(request_factory):
    return request_factory()


@pytest.fixture()
def manager_request(request_factory):
    request = request_factory()
    request.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
    yield request
    request.auth = ()
