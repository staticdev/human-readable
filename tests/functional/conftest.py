"""Fixtures for functional tests."""
import pytest
from pytest_mock import MockerFixture

import human_readable.i18n as i18n


@pytest.fixture(scope="module")
def activate_fr_fr() -> MockerFixture:
    """Activate French."""
    i18n.activate("fr_FR")
    yield None
    i18n.deactivate()


@pytest.fixture()
def activate_pt_br() -> MockerFixture:
    """Activate Brazilian Portuguese."""
    i18n.activate("pt_BR")
    yield None
    i18n.deactivate()


@pytest.fixture(scope="module")
def activate_ru_ru() -> MockerFixture:
    """Activate Russian."""
    i18n.activate("ru_RU")
    yield None
    i18n.deactivate()
