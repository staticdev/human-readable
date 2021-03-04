"""Tests for time humanizing."""
import datetime as dt

import pytest
from pytest_mock import MockerFixture

import human_readable


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (dt.timedelta(seconds=3), "3s"),
        (dt.timedelta(seconds=86400 * 476), "1y 3M"),
    ],
)
def test_date_time(
    activate_en_abbr: MockerFixture, test_input: dt.timedelta, expected: str
) -> None:
    """It returns datetime."""
    result = human_readable.date_time(test_input)

    assert result == expected
