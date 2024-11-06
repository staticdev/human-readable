"""Tests for time humanizing."""

import datetime as dt

from pytest_mock import MockerFixture

import human_readable.times as times


def test_date_time(activate_ru_ru: MockerFixture) -> None:
    """It returns datetime."""
    three_seconds = dt.timedelta(seconds=3)
    expected = "3 секунды назад"

    result = times.date_time(three_seconds)

    assert result == expected


def test_precise_delta(activate_ru_ru: MockerFixture) -> None:
    """It returns precise delta."""
    one_min_three_seconds = dt.timedelta(milliseconds=67_000)
    expected = "1 минута и 7 секунд"

    result = times.precise_delta(one_min_three_seconds)

    assert result == expected
