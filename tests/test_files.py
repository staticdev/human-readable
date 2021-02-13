# -*- coding: utf-8 -*-
"""Tests for file size humanizing."""
import human_readable.files as files


def test_file_size_singular() -> None:
    """It returns singular number."""
    assert files.file_size(1) == "1 Byte"


def test_file_size_plural() -> None:
    """It returns plural number."""
    assert files.file_size(300) == "300 Bytes"


def test_file_size_binary() -> None:
    """It returns binary format."""
    assert files.file_size(3000, True) == "2.9 KiB"


def test_file_size_gnu() -> None:
    """It returns GNU format."""
    assert files.file_size(3000000, False, True) == "2.9M"


def test_file_size_gnu_byte() -> None:
    """It returns GNU format size of byte."""
    assert files.file_size(300, False, True) == "300B"


def test_file_size_big() -> None:
    """It returns big number."""
    assert files.file_size(10 ** 26 * 30) == "3000.0 YB"


def test_file_size_formatted() -> None:
    """It returns formatted float."""
    assert files.file_size(3000, False, True, ".3f") == "2.930K"


def test_file_size_big_formatted() -> None:
    """It returns big formatted float."""
    assert files.file_size(10 ** 26 * 30, True, False, ".3f") == "2481.542 YiB"
