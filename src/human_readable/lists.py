"""Tests for lists humanization."""
from __future__ import annotations


__all__ = ["listing"]


def listing(items: list[str], separator: str, conjunction: str = "") -> str:
    """Return human readable list separated by separator.

    Optional argument is conjuntion that substitutes the last separator.

    Args:
        items: list of items.
        separator: separator of items.
        conjunction: word/string as last separator. Defaults to None.

    Returns:
        str: list in natural language.
    """
    len_items = len(items)
    if len_items == 0:
        return ""
    if len_items == 1:
        return items[0]
    phrase = items[0]
    if conjunction:
        for i in range(1, len_items - 1):
            phrase += f"{separator} {items[i]}"
        phrase += f" {conjunction} {items[len_items - 1]}"
    else:
        for i in range(1, len_items):
            phrase += f"{separator} {items[i]}"
    return phrase
