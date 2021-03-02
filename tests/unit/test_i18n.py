"""Tests for i18n."""
import pytest

import human_readable.i18n as i18n
import human_readable.numbers as numbers


DOMAIN_NAME = "humanize"
EXPECTED_MSG = (
    "Human readable cannot determinate the default location of the"
    " 'locale' folder. You need to pass the path explicitly."
)


# Internal integration tests


def test_ordinal_activate_deactivate() -> None:
    """i18n integration tests."""
    assert numbers.ordinal(5) == "5th"

    try:
        i18n.activate("ru_RU")
        assert numbers.ordinal(5) == "5ый"

    finally:
        i18n.deactivate()
        assert numbers.ordinal(5) == "5th"


def test_int_comma_activate_deactivate() -> None:
    """Int comma localization tests."""
    number = 10_000_000

    assert numbers.int_comma(number) == "10,000,000"

    try:
        i18n.activate("fr_FR")
        assert numbers.int_comma(number) == "10 000 000"

    finally:
        i18n.deactivate()
        assert numbers.int_comma(number) == "10,000,000"


def test_default_locale_path_defined__file__() -> None:
    """Test _get_default_locale_path."""
    assert i18n._get_default_locale_path() is not None


def test_default_locale_path_null__file__() -> None:
    """Test _get_default_locale_path with __file__ null."""
    i18n.__file__ = ""
    assert i18n._get_default_locale_path() is None


def test_default_locale_path_undefined__file__() -> None:
    """Test _get_default_locale_path with no __file__."""
    del i18n.__file__
    assert i18n._get_default_locale_path() is None


def test_activate_path_inexistant() -> None:
    """Test activate with wrong path."""
    with pytest.raises(Exception) as excinfo:
        i18n.activate("xx_XX", "/some/wrong/path")

    assert (
        str(excinfo.value)
        == f"[Errno 2] No translation file found for domain: '{DOMAIN_NAME}'"
    )


def test_activate_null__file__() -> None:
    """Test activate null __file__."""
    i18n.__file__ = ""

    with pytest.raises(Exception) as excinfo:
        i18n.activate("ru_RU")
    assert str(excinfo.value) == EXPECTED_MSG


def test_activate_undefined__file__() -> None:
    """Test activate no __file__."""
    del i18n.__file__

    with pytest.raises(Exception) as excinfo:
        i18n.activate("ru_RU")
    assert str(excinfo.value) == EXPECTED_MSG
