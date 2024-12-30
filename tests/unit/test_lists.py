"""Tests for listing humanization."""

from __future__ import annotations

import pytest

import human_readable.lists as lists


@pytest.mark.parametrize(
    "params, expected",
    [
        (([], ","), ""),  # empty list
        ((["jorbas"], ","), "jorbas"),  # one element
        ((["jorbas", "maria"], ","), "jorbas, maria"),  # two elements
        ((["jorbas", "maria"], ""), "jorbas maria"),  # empty separator
    ],
)
def test_listing(params: tuple[list[str], str], expected: str) -> None:
    """Listing with separator."""
    assert lists.listing(*params) == expected


@pytest.mark.parametrize(
    "params, expected",
    [
        (([], ";", "or"), ""),  # empty list
        ((["jorbas"], ";", "or"), "jorbas"),  # one element
        ((["jorbas", "maria"], ";", "or"), "jorbas or maria"),  # two elements
        (
            (["jorbas", "maria", "gustavo"], ";", "or"),
            "jorbas; maria or gustavo",
        ),  # three elements
    ],
)
def test_listing_with_conjunction(
    params: tuple[list[str], str, str], expected: str
) -> None:
    """Listing with separator and conjunction."""
    assert lists.listing(*params) == expected
