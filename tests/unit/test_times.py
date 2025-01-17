"""Tests for time humanizing."""

from __future__ import annotations

import datetime as dt
from typing import cast

import freezegun
import pytest

import human_readable.times as times


ONE_DAY_DELTA = dt.timedelta(days=1)

# In seconds
ONE_MICROSECOND = 1 / 1000000
FOUR_MICROSECONDS = 4 / 1000000
ONE_MILLISECOND = 1 / 1000
FOUR_MILLISECONDS = 4 / 1000
MICROSECONDS_101_943 = 101943 / 1000000  # 101.94 milliseconds
MILLISECONDS_1_337 = 1337 / 1000  # 1.337 seconds
ONE_HOUR = 3600
ONE_DAY = 24 * ONE_HOUR
ONE_YEAR = 365.25 * ONE_DAY

with freezegun.freeze_time("2020-02-02"):
    NOW = dt.datetime.now()
    NOW_UTC = dt.datetime.now(tz=dt.timezone.utc)
    NOW_UTC_PLUS_01_00 = dt.datetime.now(
        tz=dt.timezone(offset=dt.timedelta(hours=1))
    )
    TODAY = dt.date.today()
    TOMORROW = TODAY + ONE_DAY_DELTA
    YESTERDAY = TODAY - ONE_DAY_DELTA
    LAST_YEAR = TODAY - 365 * ONE_DAY_DELTA
    NEXT_YEAR = TODAY + 365 * ONE_DAY_DELTA
    SOME_YEAR = dt.date(1988, 11, 12)


def assert_equal_datetime(dt1: dt.datetime, dt2: dt.datetime) -> None:
    """Help to check if two datetimes are the same."""
    td = dt1 - dt2
    assert td.seconds == 0


def assert_equal_timedelta(td1: dt.timedelta, td2: dt.timedelta) -> None:
    """Help to check if two timedeltas are the same."""
    assert td1.days == td2.days
    assert td1.seconds == td2.seconds


# These are not considered "public" interfaces, but require tests anyway."""


def test_date_and_delta() -> None:
    """Tests date_and_delta utility method."""
    now = dt.datetime.now()
    tdelta = dt.timedelta
    int_tests = (3, 29, 86399, 86400, 86401 * 30)
    date_tests = [now - tdelta(seconds=x) for x in int_tests]
    td_tests = [tdelta(seconds=x) for x in int_tests]
    results = [(now - tdelta(seconds=x), tdelta(seconds=x)) for x in int_tests]
    for test in (int_tests, date_tests, td_tests):
        for arg, result in zip(test, results):
            int_arg = cast(int, arg)
            dtime, delta = times.date_and_delta(int_arg)
            assert_equal_datetime(dtime, result[0])
            assert_equal_timedelta(delta, result[1])


@pytest.mark.parametrize(
    "hour, expected",
    [
        (0, ""),
        (1, "morning"),
        (11, "morning"),
        (12, ""),
        (13, "afternoon"),
        (17, "afternoon"),
        (18, "afternoon"),
        (19, "evening"),
        (23, "evening"),
    ],
)
def test_time_of_day(hour: int, expected: str) -> None:
    """It returns period of the day."""
    assert times.time_of_day(hour) == expected


@pytest.mark.parametrize(
    "time, expected",
    [
        (dt.time(0, 30, 0), "thirty minutes past zero"),
        (dt.time(6, 59, 0), "one minute to seven hours"),
        (dt.time(13, 1, 0), "one minute past one"),
        (dt.time(4, 50, 10), "ten minutes to five hours"),
        (dt.time(11, 55, 0), "five minutes to twelve hours"),
        (dt.time(21, 0, 40), "nine o'clock"),
    ],
)
def test_timing_formal(time: dt.time, expected: str) -> None:
    """Tests timing method."""
    result = times.timing(time)

    assert result == expected


@pytest.mark.parametrize(
    "time, expected",
    [
        (dt.time(0, 30, 0), "half past midnight"),
        (dt.time(6, 35, 0), "twenty five to seven in the morning"),
        (dt.time(13, 1, 0), "one and one in the afternoon"),
        (dt.time(4, 50, 10), "ten to five in the morning"),
        (dt.time(10, 45, 0), "a quarter to eleven in the morning"),
        (dt.time(11, 55, 0), "five to noon"),
        (dt.time(12, 15, 0), "a quarter past noon"),
        (dt.time(21, 0, 40), "nine in the evening"),
        (dt.time(23, 40, 30), "twenty to midnight"),
    ],
)
def test_timing_informal(time: dt.time, expected: str) -> None:
    """Tests timing method with formal=False."""
    result = times.timing(time, formal=False)

    assert result == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "a moment"),
        (dt.timedelta(seconds=1), "a second"),
        (30, "30 seconds"),
        (dt.timedelta(minutes=1, seconds=30), "a minute"),
        (dt.timedelta(minutes=2), "2 minutes"),
        (dt.timedelta(hours=1, minutes=30, seconds=30), "an hour"),
        (dt.timedelta(hours=23, minutes=50, seconds=50), "23 hours"),
        (dt.timedelta(days=1), "a day"),
        (dt.timedelta(days=9), "9 days"),
        (dt.timedelta(days=35), "a month"),
        (dt.timedelta(days=65), "2 months"),
        (dt.timedelta(days=365), "a year"),
        (dt.timedelta(days=365 + 4), "1 year, 4 days"),
        (dt.timedelta(days=365 + 35), "1 year, 1 month"),
        (dt.timedelta(days=500), "1 year, 4 months"),
        (dt.timedelta(days=365 * 2 + 35), "2 years"),
        (dt.timedelta(seconds=30), "30 seconds"),
        (dt.timedelta(days=10000), "27 years"),
    ],
)
def test_time_delta(value: dt.timedelta | int, expected: str) -> None:
    """It returns delta in words."""
    assert times.time_delta(value) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (dt.timedelta(days=7), "7 days"),
        (dt.timedelta(days=31), "31 days"),
        (dt.timedelta(days=230), "230 days"),
        (dt.timedelta(days=400), "1 year, 35 days"),
    ],
)
def test_time_delta_no_months(test_input: dt.timedelta, expected: str) -> None:
    """Test time_delta with no months."""
    assert times.time_delta(test_input, use_months=False) == expected


@pytest.mark.parametrize(
    "minimum_unit, seconds, expected",
    [
        ("seconds", ONE_MICROSECOND, "a moment"),
        ("seconds", FOUR_MICROSECONDS, "a moment"),
        ("seconds", ONE_MILLISECOND, "a moment"),
        ("seconds", FOUR_MILLISECONDS, "a moment"),
        ("seconds", MICROSECONDS_101_943, "a moment"),  # 0.10194 s
        ("seconds", MILLISECONDS_1_337, "a second"),  # 1.337 s
        ("seconds", 2, "2 seconds"),
        ("seconds", 4, "4 seconds"),
        ("seconds", ONE_HOUR + FOUR_MILLISECONDS, "an hour"),
        ("seconds", ONE_DAY + FOUR_MILLISECONDS, "a day"),
        ("seconds", ONE_YEAR + FOUR_MICROSECONDS, "a year"),
        ("milliseconds", FOUR_MICROSECONDS, "0 milliseconds"),
        ("milliseconds", ONE_MILLISECOND, "1 millisecond"),
        ("milliseconds", FOUR_MILLISECONDS, "4 milliseconds"),
        ("milliseconds", MICROSECONDS_101_943, "101 milliseconds"),  # 101.94 ms
        ("milliseconds", MILLISECONDS_1_337, "a second"),  # 1,337 ms
        ("milliseconds", 2, "2 seconds"),
        ("milliseconds", 4, "4 seconds"),
        ("milliseconds", ONE_HOUR + FOUR_MILLISECONDS, "an hour"),
        ("milliseconds", ONE_YEAR + FOUR_MICROSECONDS, "a year"),
        ("microseconds", ONE_MICROSECOND, "1 microsecond"),
        ("microseconds", FOUR_MICROSECONDS, "4 microseconds"),
        ("microseconds", FOUR_MILLISECONDS, "4 milliseconds"),
        (
            "microseconds",
            MICROSECONDS_101_943,
            "101 milliseconds",
        ),  # 101,940 µs
        ("microseconds", MILLISECONDS_1_337, "a second"),  # 1,337,000 µs
        ("microseconds", 2, "2 seconds"),
        ("microseconds", 4, "4 seconds"),
        ("microseconds", ONE_HOUR + FOUR_MILLISECONDS, "an hour"),
        ("microseconds", ONE_DAY + FOUR_MILLISECONDS, "a day"),
        ("microseconds", ONE_YEAR + FOUR_MICROSECONDS, "a year"),
    ],
)
def test_time_delta_minimum_unit_explicit(
    minimum_unit: str, seconds: float, expected: str
) -> None:
    """Test time_delta minimum unit."""
    delta = dt.timedelta(seconds=seconds)

    assert times.time_delta(delta, minimum_unit=minimum_unit) == expected


@pytest.mark.parametrize(
    "value, when, expected",
    [
        (NOW, NOW, "a moment"),
        (NOW_UTC, NOW_UTC, "a moment"),
    ],
)
def test_time_delta_when_explicit(
    value: dt.timedelta, when: dt.datetime, expected: str
) -> None:
    """Test time_delta when."""
    assert times.time_delta(value, when=when) == expected


@pytest.mark.parametrize(
    "value, when",
    [
        (NOW_UTC, None),
        (NOW_UTC, NOW),
        (NOW_UTC_PLUS_01_00, None),
        (NOW_UTC_PLUS_01_00, NOW),
    ],
)
def test_time_delta_when_missing_tzinfo(
    value: dt.timedelta, when: dt.datetime
) -> None:
    """It raises a TypeError."""
    with pytest.raises(TypeError):
        times.time_delta(value, when=when)


def test_time_delta_high_minimum_unit() -> None:
    """It raises ValueError."""
    with pytest.raises(ValueError):
        times.time_delta(1, minimum_unit="years")


@freezegun.freeze_time("2020-02-02")
@pytest.mark.parametrize(
    "value, expected",
    [
        (NOW, "now"),
        (NOW - dt.timedelta(seconds=1), "a second ago"),
        (NOW - dt.timedelta(seconds=30), "30 seconds ago"),
        (NOW - dt.timedelta(minutes=1, seconds=30), "a minute ago"),
        (NOW - dt.timedelta(minutes=2), "2 minutes ago"),
        (NOW - dt.timedelta(hours=1, minutes=30, seconds=30), "an hour ago"),
        (NOW - dt.timedelta(hours=23, minutes=50, seconds=50), "23 hours ago"),
        (NOW - dt.timedelta(days=1), "a day ago"),
        (NOW - dt.timedelta(days=500), "1 year, 4 months ago"),
        (NOW - dt.timedelta(days=365 * 2 + 35), "2 years ago"),
        (NOW + dt.timedelta(seconds=1), "a second from now"),
        (NOW + dt.timedelta(seconds=30), "30 seconds from now"),
        (NOW + dt.timedelta(minutes=1, seconds=30), "a minute from now"),
        (NOW + dt.timedelta(minutes=2), "2 minutes from now"),
        (
            NOW + dt.timedelta(hours=1, minutes=30, seconds=30),
            "an hour from now",
        ),
        (
            NOW + dt.timedelta(hours=23, minutes=50, seconds=50),
            "23 hours from now",
        ),
        (NOW + dt.timedelta(days=1), "a day from now"),
        (NOW + dt.timedelta(days=500), "1 year, 4 months from now"),
        (NOW + dt.timedelta(days=365 * 2 + 35), "2 years from now"),
        (NOW + dt.timedelta(days=10000), "27 years from now"),
        (NOW - dt.timedelta(days=365 + 35), "1 year, 1 month ago"),
        (30, "30 seconds ago"),
        (NOW - dt.timedelta(days=365 * 2 + 65), "2 years ago"),
        (NOW - dt.timedelta(days=365 + 4), "1 year, 4 days ago"),
    ],
)
def test_date_time(
    value: dt.timedelta | int | dt.datetime, expected: str
) -> None:
    """It returns relative time."""
    assert times.date_time(value) == expected


@freezegun.freeze_time("2020-02-02")
@pytest.mark.parametrize(
    "value, expected",
    [
        (NOW, "now"),
        (NOW - dt.timedelta(seconds=1), "a second ago"),
        (NOW - dt.timedelta(seconds=30), "30 seconds ago"),
        (NOW - dt.timedelta(minutes=1, seconds=30), "a minute ago"),
        (NOW - dt.timedelta(minutes=2), "2 minutes ago"),
        (NOW - dt.timedelta(hours=1, minutes=30, seconds=30), "an hour ago"),
        (NOW - dt.timedelta(hours=23, minutes=50, seconds=50), "23 hours ago"),
        (NOW - dt.timedelta(days=1), "a day ago"),
        (NOW - dt.timedelta(days=17), "17 days ago"),
        (NOW - dt.timedelta(days=47), "47 days ago"),
        (NOW - dt.timedelta(days=500), "1 year, 135 days ago"),
        (NOW - dt.timedelta(days=365 * 2 + 35), "2 years ago"),
        (NOW + dt.timedelta(seconds=1), "a second from now"),
        (NOW + dt.timedelta(seconds=30), "30 seconds from now"),
        (NOW + dt.timedelta(minutes=1, seconds=30), "a minute from now"),
        (NOW + dt.timedelta(minutes=2), "2 minutes from now"),
        (
            NOW + dt.timedelta(hours=1, minutes=30, seconds=30),
            "an hour from now",
        ),
        (
            NOW + dt.timedelta(hours=23, minutes=50, seconds=50),
            "23 hours from now",
        ),
        (NOW + dt.timedelta(days=1), "a day from now"),
        (NOW + dt.timedelta(days=500), "1 year, 135 days from now"),
        (NOW + dt.timedelta(days=365 * 2 + 35), "2 years from now"),
        (NOW + dt.timedelta(days=10000), "27 years from now"),
        (NOW - dt.timedelta(days=365 + 35), "1 year, 35 days ago"),
        (30, "30 seconds ago"),
        (NOW - dt.timedelta(days=365 * 2 + 65), "2 years ago"),
        (NOW - dt.timedelta(days=365 + 4), "1 year, 4 days ago"),
    ],
)
def test_date_time_no_months(
    value: dt.timedelta | int | dt.datetime, expected: str
) -> None:
    """It returns relative time with no months."""
    assert times.date_time(value, use_months=False) == expected


@freezegun.freeze_time("2020-02-02")
@pytest.mark.parametrize(
    "date, expected",
    [
        (TODAY, "today"),
        (TOMORROW, "tomorrow"),
        (YESTERDAY, "yesterday"),
        (dt.date(TODAY.year, 3, 5), "Mar 05"),
    ],
)
def test_day(date: dt.date, expected: str) -> None:
    """It returns natural day."""
    assert times.day(date) == expected


def test_day_formatting() -> None:
    """It returns natural day with formatting."""
    expected = "1982.06.27"
    assert times.day(dt.date(1982, 6, 27), "%Y.%m.%d") == expected


@freezegun.freeze_time("2020-02-02")
@pytest.mark.parametrize(
    "date, expected",
    [
        (TODAY, "today"),
        (TOMORROW, "tomorrow"),
        (YESTERDAY, "yesterday"),
        (dt.date(TODAY.year, 3, 5), "Mar 05"),
        (dt.date(1982, 6, 27), "Jun 27 1982"),
        (dt.date(2019, 2, 2), "Feb 02 2019"),
        (dt.date(2019, 3, 2), "Mar 02 2019"),
        (dt.date(2019, 4, 2), "Apr 02 2019"),
        (dt.date(2019, 5, 2), "May 02 2019"),
        (dt.date(2019, 6, 2), "Jun 02 2019"),
        (dt.date(2019, 7, 2), "Jul 02 2019"),
        (dt.date(2019, 8, 2), "Aug 02 2019"),
        (dt.date(2019, 9, 2), "Sep 02 2019"),
        (dt.date(2019, 10, 2), "Oct 02"),
        (dt.date(2019, 11, 2), "Nov 02"),
        (dt.date(2019, 12, 2), "Dec 02"),
        (dt.date(2020, 1, 2), "Jan 02"),
        (dt.date(2020, 2, 2), "today"),
        (dt.date(2020, 3, 2), "Mar 02"),
        (dt.date(2020, 4, 2), "Apr 02"),
        (dt.date(2020, 5, 2), "May 02"),
        (dt.date(2020, 6, 2), "Jun 02"),
        (dt.date(2020, 7, 2), "Jul 02"),
        (dt.date(2020, 8, 2), "Aug 02 2020"),
        (dt.date(2020, 9, 2), "Sep 02 2020"),
        (dt.date(2020, 10, 2), "Oct 02 2020"),
        (dt.date(2020, 11, 2), "Nov 02 2020"),
        (dt.date(2020, 12, 2), "Dec 02 2020"),
        (dt.date(2021, 1, 2), "Jan 02 2021"),
        (dt.date(2021, 2, 2), "Feb 02 2021"),
    ],
)
def test_date(date: dt.date, expected: str) -> None:
    """It returns natural date."""
    assert times.date(date) == expected


@freezegun.freeze_time("2020-02-02")
@pytest.mark.parametrize(
    "date, expected",
    [
        (TODAY, "this year"),
        (NEXT_YEAR, "next year"),
        (LAST_YEAR, "last year"),
        (SOME_YEAR, "1988"),
    ],
)
def test_year(date: dt.date, expected: str) -> None:
    """Tests year method."""
    result = times.year(date)

    assert result == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (dt.timedelta(seconds=1), "1 second"),
        (1, "1 second"),
        (2, "2 seconds"),
        (60, "1 minute"),
        (120, "2 minutes"),
        (3600, "1 hour"),
        (3600 * 2, "2 hours"),
        (3600 * 24, "1 day"),
        (3600 * 24 * 2, "2 days"),
        (3600 * 24 * 365, "1 year"),
        (3600 * 24 * 365 * 2, "2 years"),
    ],
)
def test_precise_delta_min_seconds(
    value: dt.timedelta | int, expected: str
) -> None:
    """It returns delta with minimum_unit default to second."""
    assert times.precise_delta(value) == expected


@pytest.mark.parametrize(
    "value, min_unit, expected",
    [
        (dt.timedelta(microseconds=1), "microseconds", "1 microsecond"),
        (dt.timedelta(microseconds=2), "microseconds", "2 microseconds"),
        (dt.timedelta(microseconds=1000), "microseconds", "1 millisecond"),
        (dt.timedelta(microseconds=2000), "microseconds", "2 milliseconds"),
        (630, "minutes", "10.50 minutes"),
    ],
)
def test_precise_delta_minimum_unit(
    value: dt.timedelta | int, min_unit: str, expected: str
) -> None:
    """It returns delta considering minimum unit."""
    assert times.precise_delta(value, minimum_unit=min_unit) == expected


@pytest.mark.parametrize(
    "value, min_unit, expected",
    [
        (
            dt.timedelta(microseconds=1001),
            "microseconds",
            "1 millisecond and 1 microsecond",
        ),
        (
            dt.timedelta(microseconds=2002),
            "microseconds",
            "2 milliseconds and 2 microseconds",
        ),
        (
            dt.timedelta(seconds=1, microseconds=2),
            "microseconds",
            "1 second and 2 microseconds",
        ),
        (
            dt.timedelta(hours=4, seconds=3, microseconds=2),
            "microseconds",
            "4 hours, 3 seconds and 2 microseconds",
        ),
        (
            dt.timedelta(days=5, hours=4, seconds=3, microseconds=2),
            "microseconds",
            "5 days, 4 hours, 3 seconds and 2 microseconds",
        ),
        (
            dt.timedelta(days=370, hours=4, seconds=3, microseconds=2),
            "microseconds",
            "1 year, 5 days, 4 hours, 3 seconds and 2 microseconds",
        ),
        (
            dt.timedelta(days=370, microseconds=2),
            "microseconds",
            "1 year, 5 days and 2 microseconds",
        ),
        (
            dt.timedelta(days=370, seconds=2),
            "microseconds",
            "1 year, 5 days and 2 seconds",
        ),
        (
            dt.timedelta(seconds=0.01),
            "minutes",
            "0 minutes",
        ),
    ],
)
def test_precise_delta_combined_units(
    value: dt.timedelta | int, min_unit: str, expected: str
) -> None:
    """It returns delta with combined units."""
    assert times.precise_delta(value, minimum_unit=min_unit) == expected


@pytest.mark.parametrize(
    "value, min_unit, fmt, expected",
    [
        (
            dt.timedelta(microseconds=1001),
            "milliseconds",
            "0.4f",
            "1.0010 milliseconds",
        ),
        (
            dt.timedelta(microseconds=2002),
            "milliseconds",
            "0.4f",
            "2.0020 milliseconds",
        ),
        (
            dt.timedelta(microseconds=2002),
            "milliseconds",
            "0.2f",
            "2.00 milliseconds",
        ),
        (
            dt.timedelta(seconds=1, microseconds=230000),
            "seconds",
            "0.2f",
            "1.23 seconds",
        ),
        (
            dt.timedelta(hours=4, seconds=3, microseconds=200000),
            "seconds",
            "0.2f",
            "4 hours and 3.20 seconds",
        ),
        (
            dt.timedelta(days=5, hours=4, seconds=30 * 60),
            "seconds",
            "0.2f",
            "5 days, 4 hours and 30 minutes",
        ),
        (
            dt.timedelta(days=5, hours=4, seconds=30 * 60),
            "hours",
            "0.2f",
            "5 days and 4.50 hours",
        ),
        (
            dt.timedelta(days=5, hours=4, seconds=30 * 60),
            "days",
            "0.2f",
            "5.19 days",
        ),
        (dt.timedelta(days=120), "months", "0.2f", "3.93 months"),
        (dt.timedelta(days=183), "years", "0.1f", "0.5 years"),
    ],
)
def test_precise_delta_custom_format(
    value: dt.timedelta | int, min_unit: str, fmt: str, expected: str
) -> None:
    """It returns custom formatted delta."""
    assert (
        times.precise_delta(value, minimum_unit=min_unit, formatting=fmt)
        == expected
    )


@pytest.mark.parametrize(
    "value, min_unit, suppress, expected",
    [
        (
            dt.timedelta(microseconds=1200),
            "microseconds",
            [],
            "1 millisecond and 200 microseconds",
        ),
        (
            dt.timedelta(microseconds=1200),
            "microseconds",
            ["milliseconds"],
            "1200 microseconds",
        ),
        (
            dt.timedelta(microseconds=1200),
            "microseconds",
            ["microseconds"],
            "1.20 milliseconds",
        ),
        (
            dt.timedelta(seconds=1, microseconds=200),
            "microseconds",
            ["seconds"],
            "1000 milliseconds and 200 microseconds",
        ),
        (
            dt.timedelta(seconds=1, microseconds=200000),
            "microseconds",
            ["milliseconds"],
            "1 second and 200000 microseconds",
        ),
        (
            dt.timedelta(seconds=1, microseconds=200000),
            "microseconds",
            ["milliseconds", "microseconds"],
            "1.20 seconds",
        ),
        (
            dt.timedelta(hours=4, seconds=30, microseconds=200),
            "microseconds",
            ["microseconds"],
            "4 hours, 30 seconds and 0.20 milliseconds",
        ),
        (
            dt.timedelta(hours=4, seconds=30, microseconds=200),
            "microseconds",
            ["seconds"],
            "4 hours, 30000 milliseconds and 200 microseconds",
        ),
        (
            dt.timedelta(hours=4, seconds=30, microseconds=200),
            "microseconds",
            ["seconds", "milliseconds"],
            "4 hours and 30000200 microseconds",
        ),
        (
            dt.timedelta(hours=4, seconds=30, microseconds=200),
            "microseconds",
            ["hours"],
            "240 minutes, 30 seconds and 200 microseconds",
        ),
        (
            dt.timedelta(hours=4, seconds=30, microseconds=200),
            "microseconds",
            ["hours", "seconds", "milliseconds", "microseconds"],
            "240.50 minutes",
        ),
    ],
)
def test_precise_delta_suppress_units(
    value: dt.timedelta | int, min_unit: str, suppress: list[str], expected: str
) -> None:
    """It returns delta with supressed units."""
    assert (
        times.precise_delta(value, minimum_unit=min_unit, suppress=suppress)
        == expected
    )


def test_precise_delta_suppress_minimum_unit() -> None:
    """It raises ValueError."""
    with pytest.raises(ValueError):
        times.precise_delta(1, minimum_unit="years", suppress=["years"])


def test_unit_lt() -> None:
    """It compares two units."""
    years, minutes = times.Unit["YEARS"], times.Unit["MINUTES"]
    assert minutes < years
    assert years > minutes
    assert minutes == minutes
