"""Tests for lists humanization."""
from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Any


__all__ = ["listing"]


def listing(items: Sequence[Any], separator: Any, conjunction: Any = None, oxford: bool = False) -> str:
    """Return human readable list separated by separator.

    Optional argument is conjuntion that substitutes the last separator.

    Args:
        items: list of items.
        separator: separator of items.
        conjunction: word/string as last separator. Defaults to None.
        oxford: apply separators in the same manner as an oxford comma

    Returns:
        str: list in natural language.
    """
    len_items = len(items)
    if len_items == 0:
        return ""
    if len_items == 1:
        return str(items[0])
    phrase = str(items[0])
    if conjunction is not None:
        for i in range(1, len_items - 1):
            phrase += f"{separator} {items[i]}"
        if oxford and len_items > 2:
            phrase += str(separator)
        phrase += f" {conjunction} {items[len_items - 1]}"
    else:
        for i in range(1, len_items):
            phrase += f"{separator} {items[i]}"
    return phrase
