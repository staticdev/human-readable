"""Tests for numbers humanizing."""
from typing import Tuple
from typing import Union

import pytest

import human_readable.numbers as numbers


@pytest.mark.parametrize(
    "params, expected",
    [
        (1, "1st"),  # first suffix
        ("1", "1st"),  # str number
        (13, "13th"),  # third suffix
        (111, "111th"),  # more than hundred
    ],
)
def test_ordinal(params: int, expected: str) -> None:
    """Ordinal tests."""
    assert numbers.ordinal(params) == expected


@pytest.mark.parametrize(
    "params, expected",
    [
        (100, "100"),  # unchanged number
        (1000, "1,000"),  # number with comma
        (1000000, "1,000,000"),  # number with two commas
        (1234567.1234567, "1,234,567.1234567"),  # number with commas and dot
    ],
)
def test_int_comma(params: int, expected: str) -> None:
    """Int comma tests."""
    assert numbers.int_comma(params) == expected


@pytest.mark.parametrize(
    "params, expected",
    [
        (100, "100"),  # simple number
        (1200000, "1.2 million"),  # million number
        (8100000000000000000000000000000000, "8.1 decillion"),  # decillion number
        (10 ** 101, "1" + "0" * 101),  # very big number without suffix
        (999999999, "1.0 billion"),  # rounded up suffix
    ],
)
def test_int_word(params: int, expected: str) -> None:
    """Int word tests."""
    assert numbers.int_word(params) == expected


def test_int_word_formatted() -> None:
    """Int word with formatting tests."""
    expected = "1.23 million"
    assert numbers.int_word(1230000, "0.2f") == expected


@pytest.mark.parametrize(
    "params, expected",
    [
        (0, "zero"),  # simplest number
        ("7", "seven"),  # string number
        (10, "10"),  # bigger than 9
    ],
)
def test_ap_number(params: int, expected: str) -> None:
    """AP number tests."""
    assert numbers.ap_number(params) == expected


@pytest.mark.parametrize(
    "params, expected",
    [
        (1, "1"),  # whole number int
        (2.0, "2"),  # whole number float
        (5 / 6.0, "5/6"),  # simple fraction
        (8.9, "8 9/10"),  # compound fraction
        ("8.9", "8 9/10"),  # string fraction
    ],
)
def test_fractional(params: int, expected: str) -> None:
    """Fractional number tests."""
    assert numbers.fractional(params) == expected


@pytest.mark.parametrize(
    "params, expected",
    [
        (1000, "1.00 x 10³"),  # positive number
        ("1000", "1.00 x 10³"),  # string number
        (-1000, "1.00 x 10⁻³"),  # negative number
        (0.3, "3.00 x 10⁻¹"),  # between 0 and 1
        (5.5, "5.50 x 10⁰"),  # grater precision
        (5781651000, "5.78 x 10⁹"),  # smaller precision
        (10 ** 30, "1.00 x 10³⁰"),  # big number
        (-(10 ** 30), "1.00 x 10⁻³⁰"),  # big negative number
    ],
)
def test_scientific_notation(params: Union[float, str], expected: str) -> None:
    """Scientific notation tests."""
    assert numbers.scientific_notation(params) == expected


@pytest.mark.parametrize(
    "params, expected",
    [
        (
            (
                5781651000,
                0,
            ),
            "6 x 10⁹",
        ),
        (
            (
                "5781651000",
                0,
            ),
            "6 x 10⁹",
        ),
        (
            (
                5781651000,
                4,
            ),
            "5.7817 x 10⁹",
        ),
    ],
)
def test_scientific_notation_with_precision(
    params: Tuple[Union[float, str], int], expected: str
) -> None:
    """Scientific notation tests with specified precision."""
    assert numbers.scientific_notation(*params) == expected
