"""Bits & Bytes related humanization."""


def file_size(
    value: int,
    binary: bool = False,
    gnu: bool = False,
    formatting: str = ".1f",
    small_formatting: str = "",
) -> str:
    """Return human-readable file size.

    Format a number of byteslike a human readable filesize (eg. 10 kB).  By
    default, decimal suffixes (kB, MB) are used.  Passing binary=true will use
    binary suffixes (KiB, MiB) are used and the base will be `2**10` instead of
    `10**3`.  If ``gnu`` is True, the binary argument is ignored and GNU-style
    (``ls -sh`` style) prefixes are used (K, M) with the `2**10` definition.
    Non-gnu modes are compatible with jinja2's ``filesizeformat`` filter.
    small_formatting is used instead of formatting when the number of bytes
    is small enough that the applied suffix is B / Byte / Bytes, since files
    cannot have a decimal number of bytes in a file size

    Args:
        value: size number.
        binary: binary format. Defaults to False.
        gnu: GNU format. Defaults to False.
        formatting: format pattern (applied to a float). Defaults to ".1f".
        small_formatting: format pattern for small values (applied to an int). Defaults to "".

    Returns:
        str: file size in natural language.

    """
    if gnu:
        suffixes = ("K", "M", "G", "T", "P", "E", "Z", "Y")
    elif binary:
        suffixes = (
            " KiB",
            " MiB",
            " GiB",
            " TiB",
            " PiB",
            " EiB",
            " ZiB",
            " YiB",
        )
    else:
        suffixes = (" KB", " MB", " GB", " TB", " PB", " EB", " ZB", " YB")

    base = 1024 if (gnu or binary) else 1000

    if value == 1 and not gnu:
        return f"{1:{small_formatting}} Byte"
    if value < base and not gnu:
        return f"{value:{small_formatting}} Bytes"
    if value < base and gnu:
        return f"{value:{small_formatting}}B"

    byte_size = float(value)
    suffix = ""
    for i, suffix in enumerate(suffixes):
        unit = base ** (i + 2)
        if byte_size < unit:
            return f"{base * byte_size / unit:{formatting}}{suffix}"
    return f"{base * byte_size / unit:{formatting}}{suffix}"
