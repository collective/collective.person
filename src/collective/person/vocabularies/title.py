from collective.person.interfaces import IPersonTitle
from zope.component import getUtilitiesFor
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def title_utilities(context):
    """Vocabulary with all IPersonTitle adapters."""
    terms = []
    utilities = getUtilitiesFor(IPersonTitle)
    for token, utility in utilities:
        terms.append(SimpleTerm(token, token, utility.name))
    # Sort by title
    terms = sorted(terms, key=lambda x: x.title)
    return SimpleVocabulary(terms)
