from collective.person import PACKAGE_NAME
from zope.schema.vocabulary import SimpleVocabulary

import pytest


class TestVocabTitleUtilities:
    name = f"{PACKAGE_NAME}.title_utilities"

    @pytest.fixture(autouse=True)
    def _vocab(self, get_vocabulary, portal):
        self.vocab = get_vocabulary(self.name, portal)

    def test_vocabulary(self):
        assert self.vocab is not None
        assert isinstance(self.vocab, SimpleVocabulary)

    @pytest.mark.parametrize(
        "token",
        [
            "first_last",
            "last_first",
        ],
    )
    def test_token(self, token):
        assert token in list(self.vocab.by_token)

    @pytest.mark.parametrize(
        "token,title",
        [
            ["first_last", "First and Last Name"],
            ["last_first", "Last and First Name"],
        ],
    )
    def test_token_title(self, token, title):
        term = self.vocab.getTerm(token)
        assert title == term.title
