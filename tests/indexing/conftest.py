import pytest


@pytest.fixture()
def additional_profiles() -> list[str]:
    """List of additional profiles to apply on top of the default testing profile."""
    return [
        "collective.person:demo",
        "collective.person:catalog",
    ]
