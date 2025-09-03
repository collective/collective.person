from collective.person import PACKAGE_NAME
from plone import api
from zope.schema.vocabulary import SimpleVocabulary

import pytest


class TestVocabAvailableRoles:
    name = f"{PACKAGE_NAME}.available_roles"

    @pytest.fixture(autouse=True)
    def _vocab(self, get_vocabulary, portal):
        self.vocab = get_vocabulary(self.name, portal)

    def test_vocabulary(self):
        assert self.vocab is not None
        assert isinstance(self.vocab, SimpleVocabulary)

    @pytest.mark.parametrize(
        "token",
        [
            "member",
            "student",
        ],
    )
    def test_token(self, token):
        assert token in list(self.vocab.by_token)

    @pytest.mark.parametrize(
        "token,title",
        [
            ["member", "Team Member"],
            ["student", "Student"],
        ],
    )
    def test_token_title(self, token, title):
        term = self.vocab.getTerm(token)
        assert title == term.title


class TestVocabRoles:
    name = f"{PACKAGE_NAME}.roles"

    @pytest.fixture(autouse=True)
    def _init(self, get_vocabulary, portal, persons):
        for provider_uid in persons:
            obj = api.content.find(UID=provider_uid)[0].getObject()
            obj.reindexObject()
        self.vocab = get_vocabulary(self.name, portal)

    def test_vocabulary(self):
        assert self.vocab is not None
        assert isinstance(self.vocab, SimpleVocabulary)

    @pytest.mark.parametrize(
        "token",
        [
            "member",
        ],
    )
    def test_token(self, token):
        assert token in list(self.vocab.by_token)

    @pytest.mark.parametrize(
        "token",
        [
            "student",
        ],
    )
    def test_token_not_in(self, token):
        assert token not in list(self.vocab.by_token)

    @pytest.mark.parametrize(
        "token,title",
        [
            ["member", "Team Member"],
        ],
    )
    def test_token_title(self, token, title):
        term = self.vocab.getTerm(token)
        assert title == term.title
