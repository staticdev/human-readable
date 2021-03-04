"""Tests for ru_RU numbers humanizing."""
from pytest_mock import MockerFixture

import human_readable.numbers as numbers


def test_ordinal(activate_ru_ru: MockerFixture) -> None:
    """It returns ordinal number."""
    expected = "5ый"

    result = numbers.ordinal(5)

    assert result == expected
