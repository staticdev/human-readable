"""Tests for file size humanization."""
from __future__ import annotations

import pytest

import human_readable.files as files


@pytest.mark.parametrize(
    "params, expected",
    [
        (1, "1.0 Byte"),  # unit number
        (300, "300.0 Bytes"),  # hundreds number
        (2900000, "2.9 MB"),  # millions number
        (2000000000, "2.0 GB"),  # billions number
        (10 ** 26 * 30, "3000.0 YB"),  # giant number
    ],
)
def test_file_size(params: int, expected: str) -> None:
    """File size."""
    assert files.file_size(params) == expected


@pytest.mark.parametrize(
    "params, expected",
    [
        ((1, True), "1.0 Byte"),  # unit number
        ((300, True), "300.0 Bytes"),  # hundreds number
        ((2900000, True), "2.8 MiB"),  # millions number
        ((2000000000, True), "1.9 GiB"),  # billions number
        ((10 ** 26 * 30, True), "2481.5 YiB"),  # giant number
    ],
)
def test_file_size_binary(params: tuple[int, bool], expected: str) -> None:
    """File size binary format."""
    assert files.file_size(*params) == expected


@pytest.mark.parametrize(
    "params, expected",
    [
        ((1, False, True), "1.0B"),  # unit number
        ((300, False, True), "300.0B"),  # hundreds number
        ((2900000, False, True), "2.8M"),  # millions number
        ((2000000000, False, True), "1.9G"),  # billions number
        ((10 ** 26 * 30, False, True), "2481.5Y"),  # giant number
    ],
)
def test_file_size_gnu(params: tuple[int, bool, bool], expected: str) -> None:
    """File size GNU format."""
    assert files.file_size(*params) == expected


@pytest.mark.parametrize(
    "params, expected",
    [
        ((1, False, True, ".0f"), "1B"),  # unit number
        ((300, True, False, ".2f"), "300.00 Bytes"),  # hundreds number
        ((2900000, False, True, ".3f"), "2.766M"),  # millions number
        (
            (2000000000, True, False, ".3f"),
            "1.863 GiB",
        ),  # billions number
        ((10 ** 26 * 30, False, True, ".3f"), "2481.542Y"),  # giant number
    ],
)
def test_file_size_formatted(
    params: tuple[int, bool, bool, str], expected: str
) -> None:
    """File size with formatting."""
    assert files.file_size(*params) == expected
