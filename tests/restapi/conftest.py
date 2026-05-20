from plone import api
from plone.app.testing import SITE_OWNER_NAME

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
    content = api.content.create(container=portal, **payload)
    api.content.transition(content, transition="publish")
    return content


@pytest.fixture()
def functional_portal(functional, persons_payload, roles_vocab):
    portal = functional["portal"]
    with api.env.adopt_user(SITE_OWNER_NAME):
        # Set registry for roles
        api.portal.set_registry_record("person.roles", roles_vocab)
        # Create Content
        _create_content(portal, persons_payload[0])

    transaction.commit()
    return portal
