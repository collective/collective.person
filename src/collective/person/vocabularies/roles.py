from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def _all_roles() -> dict:
    """Return all roles from control panel."""
    registry_value = api.portal.get_registry_record("person.roles")
    items = registry_value.get("items", [])
    lang = api.portal.get_current_language()
    roles = {}
    for item in items:
        key = item["token"]
        titles = item["titles"]
        if lang not in titles:
            default_lang = next(iter(titles))
            title = titles[default_lang]
        else:
            title = titles[lang]
        roles[key] = title
    return roles


@provider(IVocabularyFactory)
def available_roles_vocabulary(context):
    """Vocabulary of all roles that could be used."""
    terms = []
    roles = _all_roles()
    for token, title in roles.items():
        terms.append(SimpleTerm(token, token, title))
    # Sort by title
    terms = sorted(terms, key=lambda x: x.title)
    return SimpleVocabulary(terms)


@provider(IVocabularyFactory)
def roles_vocabulary(context):
    """Vocabulary of roles already in use."""
    terms = []
    ct = api.portal.get_tool("portal_catalog")
    existing = ct.uniqueValuesFor("roles")
    roles = {token: title for token, title in _all_roles().items() if token in existing}
    for token, title in roles.items():
        terms.append(SimpleTerm(token, token, title))
    # Sort by title
    terms = sorted(terms, key=lambda x: x.title)
    return SimpleVocabulary(terms)
