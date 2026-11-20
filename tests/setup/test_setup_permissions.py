import pytest


PERMISSION = "collective.person: Add Person"


class TestPermissions:
    @pytest.fixture(autouse=True)
    def _setup(self, portal):
        self.portal = portal

    def _roles(self) -> set:
        return {
            r["name"]
            for r in self.portal.rolesOfPermission(PERMISSION)
            if r["selected"]
        }

    @pytest.mark.parametrize("role", ["Manager", "Site Administrator", "Contributor"])
    def test_add_person_granted(self, role: str):
        assert role in self._roles()

    @pytest.mark.parametrize(
        "role",
        [
            "Editor",
            "Owner",
            "Reader",
            "Reviewer",
            "Member",
        ],
    )
    def test_add_person_not_granted(self, role: str):
        assert role not in self._roles()
