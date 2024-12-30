"""Tests for file size humanization."""

from __future__ import annotations

import pytest

from human_readable import files


@pytest.mark.parametrize(
    "params, expected",
    [
        (1, "1 Byte"),  # unit number
        (300, "300 Bytes"),  # hundreds number
        (2900000, "2.9 MB"),  # millions number
        (2000000000, "2.0 GB"),  # billions number
        (10**26 * 30, "3000.0 YB"),  # giant number
    ],
)
def test_file_size(params: int, expected: str) -> None:
    """File size."""
    assert files.file_size(params) == expected


@pytest.mark.parametrize(
    "params, expected",
    [
        ((1, True), "1 Byte"),  # unit number
        ((300, True), "300 Bytes"),  # hundreds number
        ((2900000, True), "2.8 MiB"),  # millions number
        ((2000000000, True), "1.9 GiB"),  # billions number
        ((10**26 * 30, True), "2481.5 YiB"),  # giant number
    ],
)
def test_file_size_binary(params: tuple[int, bool], expected: str) -> None:
    """File size binary format."""
    assert files.file_size(*params) == expected


@pytest.mark.parametrize(
    "params, expected",
    [
        ((1, False, True), "1B"),  # unit number
        ((300, False, True), "300B"),  # hundreds number
        ((2900000, False, True), "2.8M"),  # millions number
        ((2000000000, False, True), "1.9G"),  # billions number
        ((10**26 * 30, False, True), "2481.5Y"),  # giant number
    ],
)
def test_file_size_gnu(params: tuple[int, bool, bool], expected: str) -> None:
    """File size GNU format."""
    assert files.file_size(*params) == expected


@pytest.mark.parametrize(
    "params, expected",
    [
        ((1, False, True, ".3f", ".1f"), "1.0B"),  # unit number (small formatting)
        (
            (999, False, False, ".3f", ".1f"),
            "999.0 Bytes",
        ),  # hundreds number (small formatting)
        (
            (1000, False, False, ".3f", ".1f"),
            "1.000 KB",
        ),  # hundreds number (small formatting boundary)
        (
            (1023, False, True, ".3f", ".1f"),
            "1023.0B",
        ),  # hundreds number (small formatting boundary)
        (
            (1024, False, True, ".3f", ".1f"),
            "1.000K",
        ),  # hundreds number (small formatting boundary)
        (
            (1023, True, False, ".3f", ".1f"),
            "1023.0 Bytes",
        ),  # hundreds number (small formatting boundary)
        (
            (1024, True, False, ".3f", ".1f"),
            "1.000 KiB",
        ),  # hundreds number (small formatting boundary)
        ((2900000, False, True, ".3f"), "2.766M"),  # millions number (large formatting)
        (
            (2000000000, True, False, ".3f"),
            "1.863 GiB",
        ),  # billions number
        ((10**26 * 30, False, True, ".3f"), "2481.542Y"),  # giant number
    ],
)
def test_file_size_formatted(
    params: tuple[int, bool, bool, str], expected: str
) -> None:
    """File size with formatting."""
    assert files.file_size(*params) == expected
