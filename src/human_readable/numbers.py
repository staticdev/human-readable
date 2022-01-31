"""Humanizing functions for numbers."""
from __future__ import annotations

import fractions
import re

import human_readable.i18n as i18n


_ = i18n.gettext
# BEWARE: by some convention this has to be N_ to be detected
# but this is not ngettext as it seems
N_ = i18n.gettext_noop
P_ = i18n.pgettext

# Mapping of locale to thousands separator
_THOUSANDS_SEPARATOR = {
    "fr_FR": " ",
}


def _thousands_separator() -> str:
    """Return the thousands separator for a locale, default to comma.

    Returns:
         str: Thousands separator.
    """
    try:
        sep = _THOUSANDS_SEPARATOR[i18n._CURRENT.locale]
    except (AttributeError, KeyError):
        sep = ","
    return sep


def ordinal(value: int | str) -> str:
    """Convert an integer to its ordinal as a string.

    1 is '1º', 2 is '2º', 3 is '3º', etc.
    Works for any integer or anything int() will turn into an integer.
    Anything other value will have nothing done to it.

    Args:
        value: integer.

    Returns:
        str: ordinal string.
    """
    suffixes = (
        P_("0", "th"),
        P_("1", "st"),
        P_("2", "nd"),
        P_("3", "rd"),
        P_("4", "th"),
        P_("5", "th"),
        P_("6", "th"),
        P_("7", "th"),
        P_("8", "th"),
        P_("9", "th"),
    )
    value = int(value)
    if value % 100 in (11, 12, 13):
        return f"{value}{suffixes[0]}"
    return f"{value}{suffixes[value % 10]}"


def int_comma(value: str | float) -> str:
    """Convert an integer to a string containing commas every three digits.

    For example, 3000 becomes '3,000' and 45000 becomes '45,000'.  To maintain
    some compatability with Django's int_comma, this function also accepts
    floats.

    Args:
        value: any number.

    Returns:
        str: formatted number with commas.
    """
    sep = _thousands_separator()
    if isinstance(value, str):
        float(value.replace(sep, ""))
    else:
        float(value)
    orig = str(value)
    new = re.sub(r"^(-?\d+)(\d{3})", rf"\g<1>{sep}\g<2>", orig)
    if orig == new:
        return new
    return int_comma(new)


POWERS = [10**x for x in (6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 100)]
HUMAN_POWERS = (
    N_("million"),
    N_("billion"),
    N_("trillion"),
    N_("quadrillion"),
    N_("quintillion"),
    N_("sextillion"),
    N_("septillion"),
    N_("octillion"),
    N_("nonillion"),
    N_("decillion"),
    N_("googol"),
)


def int_word(value: float, formatting: str = ".1f") -> str:
    """Convert a large integer to a friendly text representation.

    Works best for numbers over 1 million.
    For example, 1000000 becomes '1.0 million', 1200000 becomes
    '1.2 million' and '1200000000' becomes '1.2 billion'.
    Supports up to decillion (33 digits) and googol (100 digits).
    You can pass format to change the number of decimal or general
    format of the number portion.
    This function returns a string unless the value passed was unable to be
    coaxed into an int.

    Args:
        value: any number.
        formatting: string formatting pattern. Defaults to ".1f".

    Returns:
        str: number formatted with scale words.
    """
    if value < POWERS[0]:
        return str(value)
    for ordinal, power in enumerate(POWERS[1:], 1):
        if value < power:
            chopped = value / float(POWERS[ordinal - 1])
            if float(f"{chopped:{formatting}}") == float(10**3):
                chopped = value / float(POWERS[ordinal])
                return f"{chopped:{formatting}} {_(HUMAN_POWERS[ordinal])}"
            else:
                return f"{chopped:{formatting}} {_(HUMAN_POWERS[ordinal - 1])}"
    return str(value)


def ap_number(value: float | str) -> str | float:
    """For numbers 1-9, returns the number spelled out. Otherwise, returns the number.

    This follows Associated Press style.

    Args:
        value: any number.

    Returns:
        Union[str, float]: spelled 1-9 numbers or original number.
    """
    value = int(value)
    if not 0 <= value < 10:
        return str(value)
    return (
        _("zero"),
        _("one"),
        _("two"),
        _("three"),
        _("four"),
        _("five"),
        _("six"),
        _("seven"),
        _("eight"),
        _("nine"),
    )[value]


def fractional(value: str | float) -> str:
    """Return a human readable fractional number.

    The return can be in the form of fractions and mixed fractions.
    There will be some cases where one might not want to show ugly decimal
    places for floats and decimals.

    Pass in a string, or a number or a float, and this function returns
        a string representation of a fraction
        or whole number
        or a mixed fraction

    Examples:
        >>> fractional(0.3)
        '3/10'
        >>> fractional(1.3)
        '1 3/10'
        >>> fractional(float(1/3))
        '1/3'
        >>> fractional(1)
        '1'

    This will always return a string.

    Args:
        value: any number.

    Returns:
        str: human readable number.
    """
    number = float(value)
    whole_number = int(number)
    frac = fractions.Fraction(number - whole_number).limit_denominator(1000)
    numerator = frac.numerator
    denominator = frac.denominator
    if whole_number and not numerator and denominator == 1:
        # this means that an integer was passed in
        # or variants of that integer like 1.0000
        return f"{whole_number:.0f}"
    elif not whole_number:
        return f"{numerator:.0f}/{denominator:.0f}"
    else:
        return f"{whole_number:.0f} {numerator:.0f}/{denominator:.0f}"


def scientific_notation(value: float | str, precision: int = 2) -> str:
    """Return number in string scientific notation z.wq x 10ⁿ.

    Examples:
        >>> scientific_notation(float(0.3))
        '3.00 x 10⁻¹'
        >>> scientific_notation(int(500))
        '5.00 x 10²'
        >>> scientific_notation(-1000)
        '1.00 x 10⁻³'
        >>> scientific_notation(1000, 1)
        '1.0 x 10³'
        >>> scientific_notation(1000, 3)
        '1.000 x 10³'
        >>> scientific_notation("99")
        '9.90 x 10¹'

    Args:
        value: input number.
        precision: number of decimal for first part of the number.

    Returns:
        str: Number in scientific notation z.wq x 10ⁿ.
    """
    exponents = {
        "0": "⁰",
        "1": "¹",
        "2": "²",
        "3": "³",
        "4": "⁴",
        "5": "⁵",
        "6": "⁶",
        "7": "⁷",
        "8": "⁸",
        "9": "⁹",
        "-": "⁻",
    }
    negative = False

    if "-" in str(value):
        value = str(value).replace("-", "")
        negative = True

    if isinstance(value, str):
        value = float(value)

    precision_number = f"{value:.{precision}e}"

    significand, exponent = precision_number.split("e")
    # remove extra 0
    if exponent[1] == "0":
        exponent = exponent[0] + exponent[2:]
    # remove + sign
    if exponent[0] == "+":
        exponent = exponent[1:]

    formatted_exponent = []
    if negative:
        formatted_exponent.append(exponents["-"])

    for char in exponent:
        formatted_exponent.append(exponents[char])

    return f"{significand} x 10{''.join(formatted_exponent)}"
