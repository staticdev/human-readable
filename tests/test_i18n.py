"""Tests for i18n."""
import datetime as dt

import pytest

import human_readable.i18n as i18n
import human_readable.numbers as numbers
import human_readable.times as times

EXPECTED_MSG = (
    "Human readable cannot determinate the default location of the"
    " 'locale' folder. You need to pass the path explicitly."
)


def test_i18n() -> None:
    """i18n integration tests."""
    three_seconds = dt.timedelta(seconds=3)
    one_min_three_seconds = dt.timedelta(milliseconds=67_000)

    assert times.date_time(three_seconds) == "3 seconds ago"
    assert numbers.ordinal(5) == "5th"
    assert times.precise_delta(one_min_three_seconds) == "1 minute and 7 seconds"

    try:
        i18n.activate("ru_RU")
        assert times.date_time(three_seconds) == "3 секунды назад"
        assert numbers.ordinal(5) == "5ый"
        assert times.precise_delta(one_min_three_seconds) == "1 минута и 7 секунд"

    finally:
        i18n.deactivate()
        assert times.date_time(three_seconds) == "3 seconds ago"
        assert numbers.ordinal(5) == "5th"
        assert times.precise_delta(one_min_three_seconds) == "1 minute and 7 seconds"


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
