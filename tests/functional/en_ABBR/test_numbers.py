"""Tests for ru_RU numbers humanizing."""
from pytest_mock import MockerFixture

import human_readable


def test_int_word(activate_en_abbr: MockerFixture) -> None:
    """It returns int word number."""
    expected = "12.3 B"

    result = human_readable.int_word(12345591313)

    assert result == expected
