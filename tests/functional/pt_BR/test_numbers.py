"""Tests for pt_BR numbers humanizing."""
import pytest
from pytest_mock import MockerFixture

import human_readable.numbers as numbers


@pytest.mark.parametrize(
    "params, expected",
    [
        (1, "1º"),  # first suffix
        ("1", "1º"),  # str number
        (13, "13º"),  # third suffix
        (111, "111º"),  # more than hundred
    ],
)
def test_ordinal(activate_pt_br: MockerFixture, params: int, expected: str) -> None:
    """Ordinal tests."""
    assert numbers.ordinal(params) == expected


# TODO improve int_comma to localize for more countries and pass this test
# @pytest.mark.parametrize(
#     "params, expected",
#     [
#         (100, "100"),  # unchanged number
#         (1000, "1.000"),  # number with comma
#         (1000000, "1.000.000"),  # number with two commas
#         (1234567.1234567, "1.234.567,1234567"),  # number with commas and dot
#     ],
# )
# def test_int_comma(activate_pt_br: MockerFixture, params: int, expected: str) -> None:
#     """Int comma tests."""
#     assert numbers.int_comma(params) == expected


@pytest.mark.parametrize(
    "params, expected",
    [
        (100, "100"),  # simple number
        (1200000, "1.2 milhão"),  # million number
        (8100000000000000000000000000000000, "8.1 decilhão"),  # decillion number
        (10**101, "1" + "0" * 101),  # very big number without suffix
        (999999999, "1.0 bilhão"),  # rounded up suffix
    ],
)
def test_int_word(activate_pt_br: MockerFixture, params: int, expected: str) -> None:
    """Int word tests."""
    assert numbers.int_word(params) == expected


def test_int_word_formatted(activate_pt_br: MockerFixture) -> None:
    """Int word with formatting tests."""
    expected = "1.23 milhão"
    assert numbers.int_word(1230000, "0.2f") == expected


@pytest.mark.parametrize(
    "params, expected",
    [
        (0, "zero"),  # simplest number
        ("7", "sete"),  # string number
        (10, "10"),  # bigger than 9
    ],
)
def test_ap_number(activate_pt_br: MockerFixture, params: int, expected: str) -> None:
    """AP number tests."""
    assert numbers.ap_number(params) == expected
