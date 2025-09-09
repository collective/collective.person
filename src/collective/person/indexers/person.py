from collective.person.behaviors.person import IPersonData
from collective.person.behaviors.person import IPersonDataMarker
from collective.person.content.person import Person
from plone.app.dexterity.textindexer import utils
from plone.base.utils import safe_text
from plone.i18n.normalizer.base import mapUnicode
from plone.indexer import indexer

import re


utils.searchable(IPersonData, "title")
utils.searchable(IPersonData, "description")


def zero_fill(matchobj: re.Match) -> str:
    return matchobj.group().zfill(4)


num_sort_regex = re.compile(r"\d+")


@indexer(IPersonDataMarker)
def sortable_title(obj: Person):
    title = IPersonData(obj).title
    # Ignore case, normalize accents, strip spaces
    sortabletitle = mapUnicode(safe_text(title)).lower().strip()
    # Replace numbers with zero filled numbers
    sortabletitle = num_sort_regex.sub(zero_fill, sortabletitle)
    return sortabletitle


@indexer(IPersonDataMarker)
def title(obj: Person):
    return IPersonData(obj).title
