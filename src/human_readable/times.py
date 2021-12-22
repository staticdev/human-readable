"""Time humanizing functions."""
from __future__ import annotations

import datetime as dt
import enum
import functools
import math
from typing import Any

import human_readable.i18n as i18n


_ = i18n.gettext
P_ = i18n.pgettext
N_ = i18n.ngettext


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

    def __lt__(self, other: Any) -> Any:
        """Comparison between units."""
        return self.value < other.value


def _now() -> dt.datetime:
    return dt.datetime.now()


def time_of_day(hour: int) -> str:
    """Given current hour, returns time of the day."""
    if 0 < hour < 12:
        return _("morning")
    elif 12 < hour <= 18:
        return _("afternoon")
    elif 18 < hour <= 23:
        return _("evening")
    return ""


def _formal_time(
    value: dt.time, hour: int, count_hours: list[str], count_minutes: list[str]
) -> str:
    """Return formal timing."""
    hour_count = count_hours[hour]
    if value.minute > 30:
        reversed_minute_count = count_minutes[60 - value.minute]
        minute_translation = i18n.ngettext(
            "{amount} minute", "{amount} minutes", 60 - value.minute
        ).format(amount=reversed_minute_count)
        return i18n.ngettext(
            "{minute_translation} to {hour_count} hour",
            "{minute_translation} to {hour_count} hours",
            hour,
        ).format(minute_translation=minute_translation, hour_count=hour_count)
    elif value.minute == 0:
        return i18n.ngettext(
            "{hour_count} o'clock", "{hour_count} o'clock", hour
        ).format(hour_count=hour_count)
    else:
        minute_count = count_minutes[value.minute]
        minute_translation = i18n.ngettext(
            "{amount} minute", "{amount} minutes", value.minute
        ).format(amount=minute_count)
        return i18n.ngettext(
            "{minute_translation} past {hour_count}",
            "{minute_translation} past {hour_count}",
            hour,
        ).format(hour_count=hour_count, minute_translation=minute_translation)


def _informal_hour_count(hour: int, count_hours: list[str]) -> str:
    """Return word hour used in informal timing."""
    if hour == 0:
        hour_count = _("midnight")
    elif hour == 12:
        hour_count = _("noon")
    elif hour > 12:
        hour_count = count_hours[hour - 12]
    else:
        hour_count = count_hours[hour]
    return hour_count


def _informal_minute_count(
    value: dt.time, hour: int, hour_count: str, count_minutes: list[str]
) -> str:
    """Return messsage format informal timing based on minute count."""
    if value.minute == 0:
        clock = hour_count
    elif value.minute > 30:
        if value.minute == 45:
            reversed_minute_count = _("a quarter")
        else:
            reversed_minute_count = count_minutes[60 - value.minute]
        if hour == 0:
            clock = _("{reversed_minute_count} to midnight").format(
                reversed_minute_count=reversed_minute_count
            )
        elif hour == 12:
            clock = _("{reversed_minute_count} to noon").format(
                reversed_minute_count=reversed_minute_count
            )
        else:
            clock = i18n.ngettext(
                "{reversed_minute_count} to {hour_count}",
                "{reversed_minute_count} to {hour_count}",
                hour,
            ).format(reversed_minute_count=reversed_minute_count, hour_count=hour_count)
    elif value.minute == 30:
        clock = _("half past {hour_count}").format(hour_count=hour_count)
    elif value.minute == 15:
        clock = _("a quarter past {hour_count}").format(hour_count=hour_count)
    else:
        minute_count = count_minutes[value.minute]
        clock = _("{hour_count} and {minute_count}").format(
            hour_count=hour_count, minute_count=minute_count
        )
    return clock


def _informal_time(
    value: dt.time, hour: int, count_hours: list[str], count_minutes: list[str]
) -> str:
    """Return informal timing."""
    period = time_of_day(hour)

    hour_count = _informal_hour_count(hour, count_hours)

    clock = _informal_minute_count(value, hour, hour_count, count_minutes)

    if period:
        return _("{clock} in the {period}").format(clock=clock, period=period)
    return clock


def timing(time: dt.time, formal: bool = True) -> str:
    """Return human-readable time.

    Compares time values to present time returns representing readable of time
    with the given day period.

    Args:
        time: any datetime.
        formal: formal or informal reading. Defaults to True.

    Returns:
        str: readable time or original object.
    """
    count_hours = [
        P_("hour 0", "zero"),
        P_("hour 1", "one"),
        P_("hour 2", "two"),
        P_("hour 3", "three"),
        P_("hour 4", "four"),
        P_("hour 5", "five"),
        P_("hour 6", "six"),
        P_("hour 7", "seven"),
        P_("hour 8", "eight"),
        P_("hour 9", "nine"),
        P_("hour 10", "ten"),
        P_("hour 11", "eleven"),
        P_("hour 12", "twelve"),
        P_("hour 13", "one"),
        P_("hour 14", "two"),
        P_("hour 15", "three"),
        P_("hour 16", "four"),
        P_("hour 17", "five"),
        P_("hour 18", "six"),
        P_("hour 19", "seven"),
        P_("hour 20", "eight"),
        P_("hour 21", "nine"),
        P_("hour 22", "ten"),
        P_("hour 23", "eleven"),
    ]

    count_minutes = [
        P_("minute 0", "zero"),
        P_("minute 1", "one"),
        P_("minute 2", "two"),
        P_("minute 3", "three"),
        P_("minute 4", "four"),
        P_("minute 5", "five"),
        P_("minute 6", "six"),
        P_("minute 7", "seven"),
        P_("minute 8", "eight"),
        P_("minute 9", "nine"),
        P_("minute 10", "ten"),
        P_("minute 11", "eleven"),
        P_("minute 12", "twelve"),
        P_("minute 13", "thirteen"),
        P_("minute 14", "fourteen"),
        P_("minute 15", "fifteen"),
        P_("minute 16", "sixteen"),
        P_("minute 17", "seventeen"),
        P_("minute 18", "eighteen"),
        P_("minute 19", "nineteen"),
        P_("minute 20", "twenty"),
        P_("minute 21", "twenty one"),
        P_("minute 22", "twenty two"),
        P_("minute 23", "twenty three"),
        P_("minute 24", "twenty four"),
        P_("minute 25", "twenty five"),
        P_("minute 26", "twenty six"),
        P_("minute 27", "twenty seven"),
        P_("minute 28", "twenty eight"),
        P_("minute 29", "twenty nine"),
        P_("minute 30", "thirty"),
        P_("minute 31", "thirty one"),
        P_("minute 32", "thirty two"),
        P_("minute 33", "thirty three"),
        P_("minute 34", "thirty four"),
        P_("minute 35", "thirty five"),
        P_("minute 36", "thirty six"),
        P_("minute 37", "thirty seven"),
        P_("minute 38", "thirty eight"),
        P_("minute 39", "thirty nine"),
        P_("minute 40", "forty"),
        P_("minute 41", "forty one"),
        P_("minute 42", "forty two"),
        P_("minute 43", "forty three"),
        P_("minute 44", "forty four"),
        P_("minute 45", "forty five"),
        P_("minute 46", "forty six"),
        P_("minute 47", "forty seven"),
        P_("minute 48", "forty eight"),
        P_("minute 49", "forty nine"),
        P_("minute 50", "fifty"),
        P_("minute 51", "fifty one"),
        P_("minute 52", "fifty two"),
        P_("minute 53", "fifty three"),
        P_("minute 54", "fifty four"),
        P_("minute 55", "fifty five"),
        P_("minute 56", "fifty six"),
        P_("minute 57", "fifty seven"),
        P_("minute 58", "fifty eight"),
        P_("minute 59", "fifty nine"),
    ]

    # time relative to next hour
    if time.minute > 30:
        hour = time.hour + 1
        if hour == 24:
            hour = 0
    else:
        hour = time.hour

    if formal:
        clock = _formal_time(time, hour, count_hours, count_minutes)
    else:
        clock = _informal_time(time, hour, count_hours, count_minutes)

    return clock


def _abs_timedelta(delta: dt.timedelta) -> dt.timedelta:
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
    value: str | int | dt.datetime | dt.timedelta,
    *,
    now: dt.datetime | None = None,
) -> tuple[dt.datetime, dt.timedelta]:
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
    return date, _abs_timedelta(delta)


def _less_than_a_day(seconds: int, minimum_unit_type: Unit, delta: dt.timedelta) -> str:
    if seconds == 0:
        if minimum_unit_type == Unit.MICROSECONDS and delta.microseconds < 1000:
            return i18n.ngettext(
                "{amount} microsecond", "{amount} microseconds", delta.microseconds
            ).format(amount=delta.microseconds)
        elif minimum_unit_type == Unit.MILLISECONDS or (
            minimum_unit_type == Unit.MICROSECONDS
            and 1000 <= delta.microseconds < 1_000_000
        ):
            milliseconds = delta.microseconds / 1000
            return i18n.ngettext(
                "{amount} millisecond", "{amount} milliseconds", int(milliseconds)
            ).format(amount=int(milliseconds))
        return _("a moment")
    elif seconds == 1:
        return _("a second")
    elif seconds < 60:
        return i18n.ngettext("{amount} second", "{amount} seconds", seconds).format(
            amount=seconds
        )
    elif 60 <= seconds < 120:
        return _("a minute")
    elif 120 <= seconds < 3600:
        minutes = seconds // 60
        return i18n.ngettext("{amount} minute", "{amount} minutes", minutes).format(
            amount=minutes
        )
    elif 3600 <= seconds < 3600 * 2:
        return _("an hour")
    else:
        hours = seconds // 3600
        return i18n.ngettext("{amount} hour", "{amount} hours", hours).format(
            amount=hours
        )


def _less_than_a_year(days: int, months: int, use_months: bool) -> str:
    if days == 1:
        return _("a day")
    if not use_months:
        return i18n.ngettext("{amount} day", "{amount} days", days).format(amount=days)
    else:
        if not months:
            return i18n.ngettext("{amount} day", "{amount} days", days).format(
                amount=days
            )
        elif months == 1:
            return _("a month")
        else:
            return i18n.ngettext("{amount} month", "{amount} months", months).format(
                amount=months
            )


def _one_year(days: int, months: int, use_months: bool) -> str:
    if not months and not days:
        return _("a year")
    elif not months:
        return i18n.ngettext(
            "1 year, {amount} day", "1 year, {amount} days", days
        ).format(amount=days)
    elif use_months:
        if months == 1:
            return _("1 year, 1 month")
        else:
            return i18n.ngettext(
                "1 year, {amount} month", "1 year, {amount} months", months
            ).format(amount=months)
    else:
        return i18n.ngettext(
            "1 year, {amount} day", "1 year, {amount} days", days
        ).format(amount=days)


def time_delta(
    value: dt.timedelta | int | dt.datetime,
    use_months: bool = True,
    minimum_unit: str = "seconds",
    when: dt.datetime | None = None,
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
        minimum_unit: The lowest unit that can be used. Options: "years", "months",
            "days", "hours", "minutes", "seconds", "milliseconds" or "microseconds".
        when: Point in time relative to which _value_ is
            interpreted.  Defaults to the current time in the local timezone.

    Raises:
        ValueError: when `minimum_unit` is specified.

    Returns:
        Time representation in natural language.
    """
    tmp = Unit[minimum_unit.upper()]
    if tmp not in (Unit.SECONDS, Unit.MILLISECONDS, Unit.MICROSECONDS):
        raise ValueError(f"Minimum unit '{minimum_unit}' not supported")
    minimum_unit_type = tmp

    if isinstance(value, dt.datetime):
        if not when:
            when = _now()
        delta_value = when - value
    elif isinstance(value, int):
        delta_value = dt.timedelta(seconds=value)
    else:
        delta_value = value
    delta = _abs_timedelta(delta_value)

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
    translation = i18n.ngettext("{amount} year", "{amount} years", years)
    return translation.format(amount=years)


def date_time(
    value: dt.timedelta | int | dt.datetime,
    future: bool = False,
    use_months: bool = True,
    minimum_unit: str = "seconds",
    when: dt.datetime | None = None,
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
        Time in natural language.
    """
    now = when or _now()
    date, delta = date_and_delta(value, now=now)
    # determine tense by value only if datetime/timedelta were passed
    if isinstance(value, (dt.datetime, dt.timedelta)):
        future = date > now

    str_delta = time_delta(delta, use_months, minimum_unit, when=when)

    if str_delta == _("a moment"):
        return _("now")

    if future:
        return _("{time_difference} from now").format(time_difference=str_delta)
    else:
        return _("{time_difference} ago").format(time_difference=str_delta)


def day(date: dt.date, formatting: str = "%b %d") -> str:
    """Return human-readable day.

    For date values that are tomorrow, today or yesterday compared to
    present day returns representing string. Otherwise, returns a string
    formatted according to ``formatting``.

    Args:
        date: a date.
        formatting: chosen display format.

    Returns:
        str: date formatted in natural language.
    """
    delta = date - dt.date.today()
    if delta.days == 0:
        return _("today")
    elif delta.days == 1:
        return _("tomorrow")
    elif delta.days == -1:
        return _("yesterday")
    return date.strftime(formatting)


def date(date: dt.date) -> str:
    """Return human-readable date.

    Like ``day()``, but will append a year for dates that are a year
    ago or more.

    Args:
        date: a date.

    Returns:
        str: date in natural language.
    """
    delta = _abs_timedelta(date - dt.date.today())
    if delta.days >= 5 * 365 / 12:
        return day(date, "%b %d %Y")
    return day(date)


def year(date: dt.date) -> str:
    """Return human-readable year.

    For date values that are last year, this year or next year compared to
    present year returns representing string. Otherwise, returns a string
    formatted according to the year.

    Args:
        date: a date.

    Returns:
        Year in natural language.
    """
    delta = date.year - dt.date.today().year
    if delta == 0:
        return _("this year")
    if delta == 1:
        return _("next year")
    if delta == -1:
        return _("last year")
    return str(date.year)


def _quotient_and_remainder(
    value: float, divisor: float, unit: Unit, minimum_unit: Unit, suppress: list[Unit]
) -> tuple[float, float]:
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
    value1: float,
    value2: float,
    ratio: float,
    unit: Unit,
    min_unit: Unit,
    suppress: list[Unit],
) -> tuple[float, float]:
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


def _suitable_minimum_unit(minimum_unit: Unit, suppress: list[Unit]) -> Unit:
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


def _suppress_lower_units(min_unit: Unit, suppress: list[Unit]) -> list[Unit]:
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
    for u in Unit:  # pragma: no branch
        if u == min_unit:
            break
        suppress_set.add(u)

    return list(suppress_set)


def precise_delta(
    value: dt.timedelta | int,
    minimum_unit: str = "seconds",
    suppress: list[str] | None = None,
    formatting: str = ".2f",
) -> str:
    """Return a precise representation of a timedelta.

    >>> import datetime as dt
    >>> from human_readable.times import precise_delta
    >>> delta = dt.timedelta(seconds=3633, days=2, microseconds=123000)
    >>> precise_delta(delta)
    '2 days, 1 hour and 33.12 seconds'

    A custom `formatting` can be specified to control how the fractional part
    is represented:

    >>> precise_delta(delta, formatting=".4f")
    '2 days, 1 hour and 33.1230 seconds'

    Instead, the `minimum_unit` can be changed to have a better resolution;
    the function will still readjust the unit to use the greatest of the
    units that does not lose precision.
    For example setting microseconds but still representing the date with milliseconds:

    >>> precise_delta(delta, minimum_unit="microseconds")
    '2 days, 1 hour, 33 seconds and 123 milliseconds'

    If desired, some units can be suppressed: you will not see them represented and the
    time of the other units will be adjusted to keep representing the same timedelta:

    >>> precise_delta(delta, suppress=["days"])
    '49 hours and 33.12 seconds'

    Note that microseconds precision is lost if the seconds and all
    the units below are suppressed:

    >>> delta = dt.timedelta(seconds=90, microseconds=100)
    >>> precise_delta(delta, suppress=["seconds", "milliseconds", "microseconds"])
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
    if isinstance(value, int):
        delta = dt.timedelta(seconds=value)
    else:
        delta = value

    if not suppress:
        suppress_units = []
    else:
        suppress_units = [Unit[unit.upper()] for unit in suppress]

    # Find a suitable minimum unit (it can be greater the one that the
    # user gave us if it is suppressed).
    min_unit = Unit[minimum_unit.upper()]
    min_unit = _suitable_minimum_unit(min_unit, suppress_units)
    del minimum_unit

    # Expand the suppressed units list/set to include all the units
    # that are below the minimum unit
    ext_suppress = _suppress_lower_units(min_unit, suppress_units)

    # handy aliases
    days: float = delta.days
    secs: float = delta.seconds
    usecs: float = delta.microseconds

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

    # int rule for English / unfortunatelly ngettext does not support floats
    int_years = math.ceil(years) if years > 1 else math.floor(years) if years < 1 else 1
    int_months = (
        math.ceil(months) if months > 1 else math.floor(months) if months < 1 else 1
    )
    int_days = math.ceil(days) if days > 1 else math.floor(days) if days < 1 else 1
    int_hours = math.ceil(hours) if hours > 1 else math.floor(hours) if hours < 1 else 1
    int_minutes = (
        math.ceil(minutes) if minutes > 1 else math.floor(minutes) if minutes < 1 else 1
    )
    int_secs = math.ceil(secs) if secs > 1 else math.floor(secs) if secs < 1 else 1
    int_msecs = math.ceil(msecs) if msecs > 1 else math.floor(msecs) if msecs < 1 else 1
    int_usecs = math.ceil(usecs) if usecs > 1 else math.floor(usecs) if usecs < 1 else 1

    translations = [
        (N_("{amount} year", "{amount} years", int_years), years),
        (N_("{amount} month", "{amount} months", int_months), months),
        (N_("{amount} day", "{amount} days", int_days), days),
        (N_("{amount} hour", "{amount} hours", int_hours), hours),
        (N_("{amount} minute", "{amount} minutes", int_minutes), minutes),
        (N_("{amount} second", "{amount} seconds", int_secs), secs),
        (N_("{amount} millisecond", "{amount} milliseconds", int_msecs), msecs),
        (N_("{amount} microsecond", "{amount} microseconds", int_usecs), usecs),
    ]

    texts: list[str] = []
    for unit, fmt in zip(reversed(Unit), translations):  # pragma: no branch
        translation, amount = fmt
        if amount > 0 or (not texts and unit == min_unit):
            # apply formatting if amount of min unit is factional
            if unit == min_unit and math.modf(amount)[0] > 0:
                txt_format = translation.replace("{amount}", "{amount:{formatting}}")
                texts.append(txt_format.format(amount=amount, formatting=formatting))
            else:
                texts.append(translation.format(amount=int(amount)))

        if unit == min_unit:
            break

    if len(texts) == 1:
        return texts[0]

    head = ", ".join(texts[:-1])
    tail = texts[-1]

    return _("{head} and {tail}").format(head=head, tail=tail)
