"""Control Panel Interfaces."""

from collective.person import _
from plone.autoform import directives
from plone.schema import JSONField
from zope import schema
from zope.interface import Interface

import json


VOCABULARY_SCHEMA = json.dumps({
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "token": {"type": "string"},
                    "titles": {
                        "type": "object",
                        "properties": {
                            "lang": {"type": "string"},
                            "title": {"type": "string"},
                        },
                    },
                },
            },
        }
    },
})


class IPersonSettings(Interface):
    title_utility = schema.Choice(
        title=_("Title Utility"),
        description=_("Select the utility to use for generating person titles."),
        vocabulary="collective.person.title_utilities",
        required=True,
        default="default",
    )

    roles = JSONField(
        title=_("Roles"),
        description=_("Available types of roles"),
        required=True,
        schema=VOCABULARY_SCHEMA,
        default={
            "items": [
                {
                    "token": "member",
                    "titles": {
                        "en": "Team Member",
                    },
                },
            ]
        },
        missing_value={"items": []},
    )
    directives.widget(
        "roles",
        frontendOptions={
            "widget": "vocabularyterms",
        },
    )
