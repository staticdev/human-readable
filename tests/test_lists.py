# -*- coding: utf-8 -*-
"""Tests for listing humanizing."""
import human_readable.lists as lists


def test_listing_empty() -> None:
    """It returns empty string."""
    assert lists.listing([], "") == ""


def test_listing_one() -> None:
    """It returns one name."""
    assert lists.listing(["jorbas"], ",") == "jorbas"


def test_listing_one_with_conjunction() -> None:
    """It returns one name."""
    assert lists.listing(["Jorbas"], ",", "and") == "Jorbas"


def test_listing_two() -> None:
    """It returns two names with separator."""
    assert lists.listing(["jorbas", "maria"], ",") == "jorbas, maria"


def test_listing_many_with_conjunction() -> None:
    """It returns three names with separator and conjunction."""
    assert (
        lists.listing(["jorbas", "maria", "gustavo"], ";", "ou")
        == "jorbas; maria ou gustavo"
    )
