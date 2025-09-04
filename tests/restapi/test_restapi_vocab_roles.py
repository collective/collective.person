from collective.person import PACKAGE_NAME

import pytest


class TestVocabAvailableRoles:
    name = f"{PACKAGE_NAME}.available_roles"

    @property
    def endpoint(self):
        return f"/@vocabularies/{self.name}"

    def test_manager_can_view(self, manager_request):
        response = manager_request.get(self.endpoint)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert data["items_total"] == 2
        assert data["items"][0]["title"] == "Student"
        assert data["items"][0]["token"] == "student"  # noQA: S105
        assert data["items"][1]["title"] == "Team Member"
        assert data["items"][1]["token"] == "member"  # noQA: S105

    def test_anonymous_can_view(self, anon_request):
        response = anon_request.get(self.endpoint)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert data["items_total"] == 2
        assert data["items"][0]["title"] == "Student"
        assert data["items"][0]["token"] == "student"  # noQA: S105
        assert data["items"][1]["title"] == "Team Member"
        assert data["items"][1]["token"] == "member"  # noQA: S105

    @pytest.mark.parametrize(
        "language_code,idx,expected_title,expected_token",
        [
            ["en", 0, "Student", "student"],
            ["en", 1, "Team Member", "member"],
            ["pt_BR", 0, "Colaborador", "member"],
            ["pt_BR", 1, "Estudante", "student"],
        ],
    )
    def test_translation(
        self, request_factory, language_code, idx, expected_title, expected_token
    ):
        session = request_factory()
        session.headers["Accept-Language"] = f"{language_code};q=0.5"
        response = session.get(self.endpoint)
        data = response.json()
        assert data["items"][idx]["title"] == expected_title
        assert data["items"][idx]["token"] == expected_token


class TestVocabRoles:
    name = f"{PACKAGE_NAME}.roles"

    @property
    def endpoint(self):
        return f"/@vocabularies/{self.name}"

    def test_manager_can_view(self, manager_request):
        response = manager_request.get(self.endpoint)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "batching" not in data
        assert data["items_total"] == 1
        assert data["items"][0]["title"] == "Team Member"
        assert data["items"][0]["token"] == "member"  # noQA: S105

    def test_anonymous_can_view(self, anon_request):
        response = anon_request.get(self.endpoint)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "batching" not in data
        assert data["items_total"] == 1
        assert data["items"][0]["title"] == "Team Member"
        assert data["items"][0]["token"] == "member"  # noQA: S105

    @pytest.mark.parametrize(
        "language_code,idx,expected_title,expected_token",
        [
            ["en", 0, "Team Member", "member"],
            ["pt_BR", 0, "Colaborador", "member"],
        ],
    )
    def test_translation(
        self, request_factory, language_code, idx, expected_title, expected_token
    ):
        session = request_factory()
        session.headers["Accept-Language"] = f"{language_code};q=0.5"
        response = session.get(self.endpoint)
        data = response.json()
        assert data["items"][idx]["title"] == expected_title
        assert data["items"][idx]["token"] == expected_token
