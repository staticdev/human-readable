# -*- coding: utf-8 -*-
"""Time humanizing functions."""
import datetime as dt
import enum
import functools
import math
from typing import Any
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import human_readable.i18n as i18n


_ = i18n.gettext


MONTHS = {
    1: "janeiro",
    2: "fevereiro",
    3: "março",
    4: "abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "outubro",
    11: "novembro",
    12: "dezembro",
}

HOURS = {
    0: "zero",
    1: "uma",
    2: "duas",
    3: "três",
    4: "quatro",
    5: "cinco",
    6: "seis",
    7: "sete",
    8: "oito",
    9: "nove",
    10: "dez",
    11: "onze",
    12: "doze",
    13: "treze",
    14: "quatorze",
    15: "quinze",
    16: "dezesseis",
    17: "dezessete",
    18: "dezoito",
    19: "dezenove",
    20: "vinte",
    21: "vinte e uma",
    22: "vinte e duas",
    23: "vinte e três",
}

MINUTES = {
    1: "um",
    2: "dois",
    3: "três",
    4: "quatro",
    5: "cinco",
    6: "seis",
    7: "sete",
    8: "oito",
    9: "nove",
    10: "dez",
    11: "onze",
    12: "doze",
    13: "treze",
    14: "quatorze",
    15: "quinze",
    16: "dezesseis",
    17: "dezessete",
    18: "dezoito",
    19: "dezenove",
    20: "vinte",
    21: "vinte e um",
    22: "vinte e dois",
    23: "vinte e três",
    24: "vinte e quatro",
    25: "vinte e cinco",
    26: "vinte e seis",
    27: "vinte e sete",
    28: "vinte e oito",
    29: "vinte e nove",
    30: "trinta",
    31: "trinta e um",
    32: "trinta e dois",
    33: "trinta e três",
    34: "trinta e quatro",
    35: "trinta e cinco",
    36: "trinta e seis",
    37: "trinta e sete",
    38: "trinta e oito",
    39: "trinta e nove",
    40: "quarenta",
    41: "quarenta e um",
    42: "quarenta e dois",
    43: "quarenta e três",
    44: "quarenta e quatro",
    45: "quarenta e cinco",
    46: "quarenta e seis",
    47: "quarenta e sete",
    48: "quarenta e oito",
    49: "quarenta e nove",
    50: "cinquenta",
    51: "cinquenta e um",
    52: "cinquenta e dois",
    53: "cinquenta e três",
    54: "cinquenta e quatro",
    55: "cinquenta e cinco",
    56: "cinquenta e seis",
    57: "cinquenta e sete",
    58: "cinquenta e oito",
    59: "cinquenta e nove",
}


@functools.total_ordering
class Unit(enum.Enum):
    """Enum for minimum unit."""

    MICROSECONDS = 0
    MILLISECONDS = 1
    SECONDS = 2
    MINUTES = 3
    HOURS = 4
    DAYS = 5
    MONTHS = 6
    YEARS = 7

    def __lt__(self, other):
        """Comparison between units."""
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


def _now() -> dt.datetime:
    return dt.datetime.now()


def time_of_day(hour: int) -> str:
    """Given current hour, returns time of the day."""
    if 0 < hour < 12:
        return "manhã"
    elif 12 < hour <= 18:
        return "tarde"
    elif 18 < hour <= 23:
        return "noite"
    return ""


def _formal_time(value: dt.time, hour: int) -> str:
    clock = HOURS[hour]
    if hour in [0, 1]:
        clock += " hora"
    else:
        clock += " horas"
    if value.minute in [40, 45, 50, 55]:
        clock = MINUTES[60 - value.minute] + " minutos para " + clock
    elif value.minute == 1:
        clock += " e um minuto"
    elif value.minute != 0:
        clock += " e " + MINUTES[value.minute] + " minutos"
    return clock


def _informal_time(value: dt.time, hour: int) -> str:
    clock = HOURS[hour]
    if hour == 0:
        clock = "meia noite"
    elif hour == 12:
        clock = "meio dia"
    if value.minute in [40, 45, 50, 55]:
        clock = MINUTES[60 - value.minute] + " para " + clock
    elif value.minute == 30:
        clock += " e meia"
    elif value.minute != 0:
        clock += " e " + MINUTES[value.minute]
    return clock


def timing(time: dt.time, formal: bool = True) -> str:
    """Return human-readable time.

    Compares time values to present time returns representing readable of time
    with the given day period.

    Args:
        time: any datetime.
        formal: Formal or informal reading. Defaults to True.

    Returns:
        str: readable time or original object.
    """
    if time.minute in [40, 45, 50, 55]:
        hour = time.hour + 1
    else:
        hour = time.hour

    period = time_of_day(hour)

    if formal:
        clock = _formal_time(time, hour)
    else:
        if hour > 12:
            hour -= 12
        clock = _informal_time(time, hour)
        if period:
            clock += " da " + period

    return str(clock)


def abs_timedelta(delta: dt.timedelta) -> dt.timedelta:
    """Return an "absolute" value for a timedelta.

    Args:
        delta: relative timedelta.

    Returns:
        absolute timedelta.
    """
    if delta.days < 0:
        now = _now()
        return now - (now + delta)
    return delta


def date_and_delta(
    value: Union[str, int, dt.datetime, dt.timedelta],
    *,
    now: Optional[dt.datetime] = None,
) -> Tuple[dt.datetime, dt.timedelta]:
    """Turn a value into a date and a timedelta which represents how long ago it was."""
    if not now:
        now = _now()
    if isinstance(value, dt.datetime):
        date = value
        delta = now - value
    elif isinstance(value, dt.timedelta):
        date = now - value
        delta = value
    else:
        value = int(value)
        delta = dt.timedelta(seconds=value)
        date = now - delta
    return date, abs_timedelta(delta)


def _less_than_a_day(seconds: int, minimum_unit_type: Unit, delta: dt.timedelta) -> str:
    if seconds == 0:
        if minimum_unit_type == Unit.MICROSECONDS and delta.microseconds < 1000:
            return (
                i18n.ngettext("%d microsecond", "%d microseconds", delta.microseconds)
                % delta.microseconds
            )
        elif minimum_unit_type == Unit.MILLISECONDS or (
            minimum_unit_type == Unit.MICROSECONDS
            and 1000 <= delta.microseconds < 1_000_000
        ):
            milliseconds = delta.microseconds / 1000
            return (
                i18n.ngettext("%d millisecond", "%d milliseconds", milliseconds)
                % milliseconds
            )
        return _("a moment")
    elif seconds == 1:
        return _("a second")
    elif seconds < 60:
        return i18n.ngettext("%d second", "%d seconds", seconds) % seconds
    elif 60 <= seconds < 120:
        return _("a minute")
    elif 120 <= seconds < 3600:
        minutes = seconds // 60
        return i18n.ngettext("%d minute", "%d minutes", minutes) % minutes
    elif 3600 <= seconds < 3600 * 2:
        return _("an hour")
    elif 3600 < seconds:
        hours = seconds // 3600
        return i18n.ngettext("%d hour", "%d hours", hours) % hours


def _less_than_a_year(days: int, months: int, use_months: bool) -> str:
    if days == 1:
        return _("a day")
    if not use_months:
        return i18n.ngettext("%d day", "%d days", days) % days
    else:
        if not months:
            return i18n.ngettext("%d day", "%d days", days) % days
        elif months == 1:
            return _("a month")
        else:
            return i18n.ngettext("%d month", "%d months", months) % months


def _one_year(days: int, months: int, use_months: bool) -> str:
    if not months and not days:
        return _("a year")
    elif not months:
        return i18n.ngettext("1 year, %d day", "1 year, %d days", days) % days
    elif use_months:
        if months == 1:
            return _("1 year, 1 month")
        else:
            return (
                i18n.ngettext("1 year, %d month", "1 year, %d months", months) % months
            )
    else:
        return i18n.ngettext("1 year, %d day", "1 year, %d days", days) % days


def time_delta(
    value: dt.timedelta,
    use_months: bool = True,
    minimum_unit: str = "seconds",
    when: Optional[dt.timedelta] = None,
) -> str:
    """Return human-readable time difference.

    Given a timedelta or a number of seconds, return a natural
    representation of the amount of time elapsed. This is similar to
    ``date_time``, but does not add tense to the result. If ``use_months``
    is True, then a number of months (based on 30.5 days) will be used
    for fuzziness between years.

    Args:
        value: A timedelta or a number of seconds.
        use_months: If `True`, then a number of months (based on 30.5 days) will be
            used for fuzziness between years.
        minimum_unit: The lowest unit that can be used.
        when: Point in time relative to which _value_ is
            interpreted.  Defaults to the current time in the local timezone.

    Raises:
        ValueError: when `minimum_unit` is specified.

    Returns:
        str: time representation in natural language.
    """
    tmp = Unit[minimum_unit.upper()]
    if tmp not in (Unit.SECONDS, Unit.MILLISECONDS, Unit.MICROSECONDS):
        raise ValueError(f"Minimum unit '{minimum_unit}' not supported")
    minimum_unit_type = tmp

    date, delta = date_and_delta(value, now=when)
    if date is None:
        return value

    seconds = abs(delta.seconds)
    days = abs(delta.days)
    years = days // 365
    days = days % 365
    months = int(days // 30.5)

    if not years and days < 1:
        return _less_than_a_day(seconds, minimum_unit_type, delta)
    elif years == 0:
        return _less_than_a_year(days, months, use_months)
    elif years == 1:
        return _one_year(days, months, use_months)
    return i18n.ngettext(f"{years} year", f"{years} years", years)


def date_time(
    value: Any,
    future: bool = False,
    use_months: bool = True,
    minimum_unit: str = "seconds",
    when: dt.datetime = None,
) -> str:
    """Return human-readable time.

    Given a datetime or a number of seconds, return a natural representation
    of that time in a resolution that makes sense. This is more or less
    compatible with Django's ``natural_time`` filter. ``future`` is ignored for
    datetimes, where the tense is always figured out based on the current time.
    If an integer is passed, the return value will be past tense by default,
    unless ``future`` is set to True.

    Args:
        value: time value.
        future: if false uses past tense. Defaults to False.
        use_months: if true return number of months. Defaults to True.
        minimum_unit: The lowest unit that can be used.
        when: Point in time relative to which _value_ is
            interpreted.  Defaults to the current time in the local timezone.

    Returns:
        str: time in natural language.
    """
    now = when or _now()
    date, delta = date_and_delta(value, now=now)
    if date is None:
        return value
    # determine tense by value only if datetime/timedelta were passed
    if isinstance(value, (dt.datetime, dt.timedelta)):
        future = date > now

    ago = _("%s from now") if future else _("%s ago")
    delta = time_delta(delta, use_months, minimum_unit, when=when)

    if delta == _("a moment"):
        return _("now")

    return ago % delta


def day(date: dt.date, has_year: bool = False) -> str:
    """Return human-readable day.

    For date values that are tomorrow, today or yesterday compared to
    present day returns representing string. Otherwise, returns a string
    formatted according to ``formatting``.

    Args:
        date: a date.
        has_year: if year is added. Defaults to False.

    Returns:
        str: date formatted in natural language.
    """
    delta = date - dt.date.today()
    if delta.days == 0:
        return "hoje"
    if delta.days == 1:
        return "amanhã"
    if delta.days == -1:
        return "ontem"
    month = MONTHS[date.month]
    natday = "{0} de {1}".format(date.day, month)
    if has_year:
        natday += " de {0}".format(date.year)
    return natday


def year(date: dt.date) -> str:
    """Return human-readable year.

    For date values that are last year, this year or next year compared to
    present year returns representing string. Otherwise, returns a string
    formatted according to the year.

    Args:
        date: a date.

    Returns:
        str: year in natural language.
    """
    delta = date.year - dt.date.today().year
    if delta == 0:
        return "este ano"
    if delta == 1:
        return "ano que vem"
    if delta == -1:
        return "ano passado"
    return str(date.year)


def date(date: dt.date) -> str:
    """Return human-readable date.

    Like ``day()``, but will append a year for dates that are a year
    ago or more.

    Args:
        date: a date.

    Returns:
        str: date in natural language.
    """
    delta = abs_timedelta(date - dt.date.today())
    if delta.days >= 365:
        return day(date, True)
    return day(date)


def _quotient_and_remainder(
    value: int, divisor: int, unit: Unit, minimum_unit: Unit, suppress: List[Unit]
) -> Tuple[int, int]:
    """Divide `value` by `divisor` returning the quotient and remainder.

    If `unit` is `minimum_unit`, makes the quotient a float number and the remainder
    will be zero. The rational is that if `unit` is the unit of the quotient, we cannot
    represent the remainder because it would require a unit smaller than the
    `minimum_unit`.

    Example:
        >>> _quotient_and_remainder(36, 24, Unit.DAYS, Unit.DAYS, [])
        (1.5, 0)

    If unit is in `suppress`, the quotient will be zero and the remainder will be the
    initial value. The idea is that if we cannot use `unit`, we are forced to use a
    lower unit so we cannot do the division.

    Example:
        >>> _quotient_and_remainder(36, 24, Unit.DAYS, Unit.HOURS, [Unit.DAYS])
        (0, 36)

    In other case return quotient and remainder as `divmod` would do it.

    Example:
        >>> _quotient_and_remainder(36, 24, Unit.DAYS, Unit.HOURS, [])
        (1, 12)

    Args:
        value: integer value.
        divisor: the divisor.
        minimum_unit: minimum unit.
        unit: the unit of the quotient.
        suppress: list of units to be suppressed.

    Returns:
        Quotient and reminder tuple.
    """
    if unit == minimum_unit:
        return (value / divisor, 0)
    elif unit in suppress:
        return (0, value)
    else:
        return divmod(value, divisor)


def _carry(
    value1: int,
    value2: int,
    ratio: int,
    unit: Unit,
    min_unit: Unit,
    suppress: List[Unit],
) -> Tuple[float, int]:
    """Return a tuple with two values.

    If the unit is in `suppress`, multiply `value1` by `ratio` and add it to `value2`
    (carry to right). The idea is that if we cannot represent `value1` we need to
    represent it in a lower unit.
    >>> from human_readable.times import _carry, Unit
    >>> _carry(2, 6, 24, Unit.DAYS, Unit.SECONDS, [Unit.DAYS])
    (0, 54)

    If the unit is the minimum unit, `value2` is divided by `ratio` and added to
    `value1` (carry to left). We assume that `value2` has a lower unit so we need to
    carry it to `value1`.
    >>> _carry(2, 6, 24, Unit.DAYS, Unit.DAYS, [])
    (2.25, 0)

    Otherwise, just return the same input:
    >>> _carry(2, 6, 24, Unit.DAYS, Unit.SECONDS, [])
    (2, 6)

    Args:
        value1: one integer.
        value2: other integer.
        ratio: multiply ratio.
        unit: the unit of the quotient.
        min_unit: minimum unit.
        suppress: list of units to be suppressed.

    Returns:
        Carry left and carry right.
    """
    if unit == min_unit:
        return (value1 + value2 / ratio, 0)
    elif unit in suppress:
        return (0, value2 + value1 * ratio)
    else:
        return (value1, value2)


def _suitable_minimum_unit(minimum_unit: Unit, suppress: List[Unit]) -> Unit:
    """Return a minimum unit suitable that is not suppressed.

    If not suppressed, return the same unit:
    >>> from human_readable.times import _suitable_minimum_unit, Unit
    >>> _suitable_minimum_unit(Unit.HOURS, [])
    <Unit.HOURS: 4>

    But if suppressed, find a unit greather than the original one that is not
    suppressed:
    >>> _suitable_minimum_unit(Unit.HOURS, [Unit.HOURS])
    <Unit.DAYS: 5>
    >>> _suitable_minimum_unit(Unit.HOURS, [Unit.HOURS, Unit.DAYS])
    <Unit.MONTHS: 6>

    Args:
        minimum_unit: minimum unit.
        suppress: list of units to be suppressed.

    Raises:
        ValueError: when there is not suitable minimum unit given suppress.

    Returns:
        Minimum unit suitable that is not suppressed.
    """
    if minimum_unit in suppress:
        for unit in Unit:
            if unit > minimum_unit and unit not in suppress:
                return unit

        raise ValueError(
            "Minimum unit is suppressed and no suitable replacement was found."
        )

    return minimum_unit


def _suppress_lower_units(min_unit: Unit, suppress: List[Unit]) -> List[Unit]:
    """Extend suppressed units (if any) with all units lower than the minimum unit.

    >>> from human_readable.times import _suppress_lower_units, Unit
    >>> sorted(_suppress_lower_units(Unit.SECONDS, [Unit.DAYS]))
    [<Unit.MICROSECONDS: 0>, <Unit.MILLISECONDS: 1>, <Unit.DAYS: 5>]

    Args:
        min_unit: minimum unit.
        suppress: list of units to be suppressed.

    Returns:
        New suppress list.
    """
    suppress_set = set(suppress)
    for u in Unit:
        if u == min_unit:
            break
        suppress_set.add(u)

    return list(suppress_set)


def precise_delta(
    value: dt.timedelta,
    minimum_unit: str = "seconds",
    suppress: Optional[List[Unit]] = None,
    formatting: str = "%0.2f",
):
    """Return a precise representation of a timedelta.

    >>> import datetime as dt
    >>> from human_readable.times import precise_delta
    >>> delta = dt.timedelta(seconds=3633, days=2, microseconds=123000)
    >>> precise_delta(delta)
    '2 days, 1 hour and 33.12 seconds'

    A custom `formatting` can be specified to control how the fractional part
    is represented:

    >>> precise_delta(delta, formatting="%0.4f")
    '2 days, 1 hour and 33.1230 seconds'

    Instead, the `minimum_unit` can be changed to have a better resolution;
    the function will still readjust the unit to use the greatest of the
    units that does not lose precision.
    For example setting microseconds but still representing the date with milliseconds:

    >>> precise_delta(delta, minimum_unit="microseconds")
    '2 days, 1 hour, 33 seconds and 123 milliseconds'

    If desired, some units can be suppressed: you will not see them represented and the
    time of the other units will be adjusted to keep representing the same timedelta:

    >>> precise_delta(delta, suppress=['days'])
    '49 hours and 33.12 seconds'

    Note that microseconds precision is lost if the seconds and all
    the units below are suppressed:

    >>> delta = dt.timedelta(seconds=90, microseconds=100)
    >>> precise_delta(delta, suppress=['seconds', 'milliseconds', 'microseconds'])
    '1.50 minutes'

    If the delta is too small to be represented with the minimum unit,
    a value of zero will be returned:

    >>> delta = dt.timedelta(seconds=1)
    >>> precise_delta(delta, minimum_unit="minutes")
    '0.02 minutes'
    >>> delta = dt.timedelta(seconds=0.1)
    >>> precise_delta(delta, minimum_unit="minutes")
    '0 minutes'

    Args:
        value: a time delta.
        minimum_unit: minimum unit.
        suppress: list of units to be suppressed.
        formatting: standard Python format.

    Returns:
        Humanized time delta.
    """
    date, delta = date_and_delta(value)
    if date is None:
        return value

    if not suppress:
        suppress = []
    suppress = [Unit[s.upper()] for s in suppress]

    # Find a suitable minimum unit (it can be greater the one that the
    # user gave us if it is suppressed).
    min_unit = Unit[minimum_unit.upper()]
    min_unit = _suitable_minimum_unit(min_unit, suppress)
    del minimum_unit

    # Expand the suppressed units list/set to include all the units
    # that are below the minimum unit
    ext_suppress = _suppress_lower_units(min_unit, suppress)

    # handy aliases
    days = delta.days
    secs = delta.seconds
    usecs = delta.microseconds

    MICROSECONDS, MILLISECONDS, SECONDS, MINUTES, HOURS, DAYS, MONTHS, YEARS = list(
        Unit
    )

    # Given DAYS compute YEARS and the remainder of DAYS as follows:
    #   if YEARS is the minimum unit, we cannot use DAYS so
    #   we will use a float for YEARS and 0 for DAYS:
    #       years, days = years/days, 0
    #
    #   if YEARS is suppressed, use DAYS:
    #       years, days = 0, days
    #
    #   otherwise:
    #       years, days = divmod(years, days)
    #
    # The same applies for months, hours, minutes and milliseconds below
    years, days = _quotient_and_remainder(days, 365, YEARS, min_unit, ext_suppress)
    months, days = _quotient_and_remainder(days, 30.5, MONTHS, min_unit, ext_suppress)

    # If DAYS is not in suppress, we can represent the days but
    # if it is a suppressed unit, we need to carry it to a lower unit,
    # seconds in this case.
    #
    # The same applies for secs and usecs below
    days, secs = _carry(days, secs, 24 * 3600, DAYS, min_unit, ext_suppress)

    hours, secs = _quotient_and_remainder(secs, 3600, HOURS, min_unit, ext_suppress)
    minutes, secs = _quotient_and_remainder(secs, 60, MINUTES, min_unit, ext_suppress)

    secs, usecs = _carry(secs, usecs, 1e6, SECONDS, min_unit, ext_suppress)

    msecs, usecs = _quotient_and_remainder(
        usecs, 1000, MILLISECONDS, min_unit, ext_suppress
    )

    # if _unused != 0 we had lost some precision
    usecs, _unused = _carry(usecs, 0, 1, MICROSECONDS, min_unit, ext_suppress)

    fmts = [
        ("%d year", "%d years", years),
        ("%d month", "%d months", months),
        ("%d day", "%d days", days),
        ("%d hour", "%d hours", hours),
        ("%d minute", "%d minutes", minutes),
        ("%d second", "%d seconds", secs),
        ("%d millisecond", "%d milliseconds", msecs),
        ("%d microsecond", "%d microseconds", usecs),
    ]

    texts = []
    for unit, fmt in zip(reversed(Unit), fmts):
        singular_txt, plural_txt, value = fmt
        if value > 0 or (not texts and unit == min_unit):
            fmt_txt = i18n.ngettext(singular_txt, plural_txt, value)
            if unit == min_unit and math.modf(value)[0] > 0:
                fmt_txt = fmt_txt.replace("%d", formatting)

            texts.append(fmt_txt % value)

        if unit == min_unit:
            break

    if len(texts) == 1:
        return texts[0]

    head = ", ".join(texts[:-1])
    tail = texts[-1]

    return _("%s and %s") % (head, tail)
