"""Tests for fr_FR numbers humanizing."""

from pytest_mock import MockerFixture

import human_readable.numbers as numbers


def test_int_comma(activate_fr_fr: MockerFixture) -> None:
    """Int comma localization tests."""
    number = 10_000_000
    expected = "10 000 000"

    result = numbers.int_comma(number)

    assert result == expected
