"""Tests for pt_BR time humanizing."""
import datetime as dt
from typing import Union

import freezegun
import pytest
from pytest_mock import MockerFixture

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
    NOW_UTC_PLUS_01_00 = dt.datetime.now(tz=dt.timezone(offset=dt.timedelta(hours=1)))
    TODAY = dt.date.today()
    TOMORROW = TODAY + ONE_DAY_DELTA
    YESTERDAY = TODAY - ONE_DAY_DELTA


class FakeDate:
    """Test helper to fake date."""

    def __init__(self, year: int, month: int, day: int) -> None:
        """Initializes fake date."""
        self.year, self.month, self.day = year, month, day


def assert_equal_datetime(dt1: dt.datetime, dt2: dt.datetime) -> None:
    """Helper method to check if two datetimes are the same."""
    td = dt1 - dt2
    assert td.seconds == 0


def assert_equal_timedelta(td1: dt.timedelta, td2: dt.timedelta) -> None:
    """Helper method to check if two timedeltas are the same."""
    assert td1.days == td2.days
    assert td1.seconds == td2.seconds


class FakeTime:
    """Test helper class to fake time."""

    def __init__(self, hour: int, minute: int, second: int) -> None:
        """Initializes fake time."""
        self.hour, self.minute, self.second = hour, minute, second


@pytest.mark.parametrize(
    "hour, expected",
    [
        (0, ""),
        (1, "manhã"),
        (11, "manhã"),
        (12, ""),
        (13, "tarde"),
        (17, "tarde"),
        (18, "tarde"),
        (19, "noite"),
        (23, "noite"),
    ],
)
def test_time_of_day(activate_pt_br: MockerFixture, hour: int, expected: str) -> None:
    """It returns period of the day."""
    assert times.time_of_day(hour) == expected


@pytest.mark.parametrize(
    "time, expected",
    [
        (dt.time(0, 30, 0), "zero hora e trinta minutos"),
        (dt.time(6, 59, 0), "um minuto para as sete horas"),
        (dt.time(13, 1, 0), "treze horas e um minuto"),
        (dt.time(4, 50, 10), "dez minutos para as cinco horas"),
        (dt.time(11, 55, 0), "cinco minutos para as doze horas"),
        (dt.time(21, 0, 40), "vinte e uma horas"),
    ],
)
def test_timing_formal(
    activate_pt_br: MockerFixture, time: dt.time, expected: str
) -> None:
    """Tests timing method."""
    result = times.timing(time)

    assert result == expected


@pytest.mark.parametrize(
    "time, expected",
    [
        (dt.time(0, 30, 0), "meia-noite e meia"),
        (dt.time(6, 35, 0), "vinte e cinco para as sete da manhã"),
        (dt.time(13, 1, 0), "uma e um da tarde"),
        (dt.time(4, 50, 10), "dez para as cinco da manhã"),
        (dt.time(10, 45, 0), "quinze para as onze da manhã"),
        (dt.time(11, 55, 0), "cinco para o meio-dia"),
        (dt.time(12, 15, 0), "meio-dia e quinze"),
        (dt.time(21, 0, 40), "nove da noite"),
    ],
)
def test_timing_informal(
    activate_pt_br: MockerFixture, time: dt.time, expected: str
) -> None:
    """Tests timing method with formal=False."""
    result = times.timing(time, formal=False)

    assert result == expected


# @pytest.mark.parametrize(
#     "value, expected",
#     [
#         (0, "a moment"),
#         (1, "a second"),
#         (30, "30 seconds"),
#         (dt.timedelta(minutes=1, seconds=30), "a minute"),
#         (dt.timedelta(minutes=2), "2 minutes"),
#         (dt.timedelta(hours=1, minutes=30, seconds=30), "an hour"),
#         (dt.timedelta(hours=23, minutes=50, seconds=50), "23 hours"),
#         (dt.timedelta(days=1), "a day"),
#         (dt.timedelta(days=500), "1 year, 4 months"),
#         (dt.timedelta(days=365 * 2 + 35), "2 years"),
#         (dt.timedelta(seconds=1), "a second"),
#         (dt.timedelta(seconds=30), "30 seconds"),
#         (dt.timedelta(minutes=1, seconds=30), "a minute"),
#         (dt.timedelta(minutes=2), "2 minutes"),
#         (dt.timedelta(hours=1, minutes=30, seconds=30), "an hour"),
#         (dt.timedelta(hours=23, minutes=50, seconds=50), "23 hours"),
#         (dt.timedelta(days=500), "1 year, 4 months"),
#         (dt.timedelta(days=365 * 2 + 35), "2 years"),
#         (dt.timedelta(days=10000), "27 years"),
#         (dt.timedelta(days=365 + 35), "1 year, 1 month"),
#         (dt.timedelta(days=365 * 2 + 65), "2 years"),
#         (dt.timedelta(days=365 + 4), "1 year, 4 days"),
#         (dt.timedelta(days=35), "a month"),
#         (dt.timedelta(days=65), "2 months"),
#         (dt.timedelta(days=9), "9 days"),
#         (dt.timedelta(days=365), "a year"),
#     ],
# )
# def test_time_delta(value: Union[dt.timedelta, int], expected: str) -> None:
#     """It returns delta in words."""
#     assert times.time_delta(value) == expected


# @pytest.mark.parametrize(
#     "test_input, expected",
#     [
#         (dt.timedelta(days=7), "7 days"),
#         (dt.timedelta(days=31), "31 days"),
#         (dt.timedelta(days=230), "230 days"),
#         (dt.timedelta(days=400), "1 year, 35 days"),
#     ],
# )
# def test_time_delta_no_months(test_input: dt.timedelta, expected: str) -> None:
#     """Test time_delta with no months."""
#     assert times.time_delta(test_input, use_months=False) == expected


# @pytest.mark.parametrize(
#     "minimum_unit, seconds, expected",
#     [
#         ("seconds", ONE_MICROSECOND, "a moment"),
#         ("seconds", FOUR_MICROSECONDS, "a moment"),
#         ("seconds", ONE_MILLISECOND, "a moment"),
#         ("seconds", FOUR_MILLISECONDS, "a moment"),
#         ("seconds", MICROSECONDS_101_943, "a moment"),  # 0.10194 s
#         ("seconds", MILLISECONDS_1_337, "a second"),  # 1.337 s
#         ("seconds", 2, "2 seconds"),
#         ("seconds", 4, "4 seconds"),
#         ("seconds", ONE_HOUR + FOUR_MILLISECONDS, "an hour"),
#         ("seconds", ONE_DAY + FOUR_MILLISECONDS, "a day"),
#         ("seconds", ONE_YEAR + FOUR_MICROSECONDS, "a year"),
#         ("milliseconds", FOUR_MICROSECONDS, "0 milliseconds"),
#         ("milliseconds", ONE_MILLISECOND, "1 millisecond"),
#         ("milliseconds", FOUR_MILLISECONDS, "4 milliseconds"),
#         ("milliseconds", MICROSECONDS_101_943, "101 milliseconds"),  # 101.94 ms
#         ("milliseconds", MILLISECONDS_1_337, "a second"),  # 1,337 ms
#         ("milliseconds", 2, "2 seconds"),
#         ("milliseconds", 4, "4 seconds"),
#         ("milliseconds", ONE_HOUR + FOUR_MILLISECONDS, "an hour"),
#         ("milliseconds", ONE_YEAR + FOUR_MICROSECONDS, "a year"),
#         ("microseconds", ONE_MICROSECOND, "1 microsecond"),
#         ("microseconds", FOUR_MICROSECONDS, "4 microseconds"),
#         ("microseconds", FOUR_MILLISECONDS, "4 milliseconds"),
#         ("microseconds", MICROSECONDS_101_943, "101 milliseconds"),  # 101,940 µs
#         ("microseconds", MILLISECONDS_1_337, "a second"),  # 1,337,000 µs
#         ("microseconds", 2, "2 seconds"),
#         ("microseconds", 4, "4 seconds"),
#         ("microseconds", ONE_HOUR + FOUR_MILLISECONDS, "an hour"),
#         ("microseconds", ONE_DAY + FOUR_MILLISECONDS, "a day"),
#         ("microseconds", ONE_YEAR + FOUR_MICROSECONDS, "a year"),
#     ],
# )
# def test_time_delta_minimum_unit_explicit(
#     minimum_unit: str, seconds: float, expected: str
# ) -> None:
#     """Test time_delta minimum unit."""
#     delta = dt.timedelta(seconds=seconds)

#     assert times.time_delta(delta, minimum_unit=minimum_unit) == expected


# @pytest.mark.parametrize(
#     "value, when, expected",
#     [
#         (NOW, NOW, "a moment"),
#         (NOW_UTC, NOW_UTC, "a moment"),
#     ],
# )
# def test_time_delta_when_explicit(
#     value: dt.timedelta, when: dt.datetime, expected: str
# ) -> None:
#     """Test time_delta when."""
#     assert times.time_delta(value, when=when) == expected

# def test_time_delta_high_minimum_unit() -> None:
#     """It raises ValueError."""
#     with pytest.raises(ValueError):
#         times.time_delta(1, minimum_unit="years")


# @freezegun.freeze_time("2020-02-02")
# @pytest.mark.parametrize(
#     "value, expected",
#     [
#         (NOW, "now"),
#         (NOW - dt.timedelta(seconds=1), "a second ago"),
#         (NOW - dt.timedelta(seconds=30), "30 seconds ago"),
#         (NOW - dt.timedelta(minutes=1, seconds=30), "a minute ago"),
#         (NOW - dt.timedelta(minutes=2), "2 minutes ago"),
#         (NOW - dt.timedelta(hours=1, minutes=30, seconds=30), "an hour ago"),
#         (NOW - dt.timedelta(hours=23, minutes=50, seconds=50), "23 hours ago"),
#         (NOW - dt.timedelta(days=1), "a day ago"),
#         (NOW - dt.timedelta(days=500), "1 year, 4 months ago"),
#         (NOW - dt.timedelta(days=365 * 2 + 35), "2 years ago"),
#         (NOW + dt.timedelta(seconds=1), "a second from now"),
#         (NOW + dt.timedelta(seconds=30), "30 seconds from now"),
#         (NOW + dt.timedelta(minutes=1, seconds=30), "a minute from now"),
#         (NOW + dt.timedelta(minutes=2), "2 minutes from now"),
#         (NOW + dt.timedelta(hours=1, minutes=30, seconds=30), "an hour from now"),
#         (NOW + dt.timedelta(hours=23, minutes=50, seconds=50), "23 hours from now"),
#         (NOW + dt.timedelta(days=1), "a day from now"),
#         (NOW + dt.timedelta(days=500), "1 year, 4 months from now"),
#         (NOW + dt.timedelta(days=365 * 2 + 35), "2 years from now"),
#         (NOW + dt.timedelta(days=10000), "27 years from now"),
#         (NOW - dt.timedelta(days=365 + 35), "1 year, 1 month ago"),
#         (30, "30 seconds ago"),
#         (NOW - dt.timedelta(days=365 * 2 + 65), "2 years ago"),
#         (NOW - dt.timedelta(days=365 + 4), "1 year, 4 days ago"),
#     ],
# )
# def test_time(value: Union[dt.timedelta, int, dt.datetime], expected: str) -> None:
#     """It returns relative time."""
#     assert times.date_time(value) == expected


# @freezegun.freeze_time("2020-02-02")
# @pytest.mark.parametrize(
#     "value, expected",
#     [
#         (NOW, "now"),
#         (NOW - dt.timedelta(seconds=1), "a second ago"),
#         (NOW - dt.timedelta(seconds=30), "30 seconds ago"),
#         (NOW - dt.timedelta(minutes=1, seconds=30), "a minute ago"),
#         (NOW - dt.timedelta(minutes=2), "2 minutes ago"),
#         (NOW - dt.timedelta(hours=1, minutes=30, seconds=30), "an hour ago"),
#         (NOW - dt.timedelta(hours=23, minutes=50, seconds=50), "23 hours ago"),
#         (NOW - dt.timedelta(days=1), "a day ago"),
#         (NOW - dt.timedelta(days=17), "17 days ago"),
#         (NOW - dt.timedelta(days=47), "47 days ago"),
#         (NOW - dt.timedelta(days=500), "1 year, 135 days ago"),
#         (NOW - dt.timedelta(days=365 * 2 + 35), "2 years ago"),
#         (NOW + dt.timedelta(seconds=1), "a second from now"),
#         (NOW + dt.timedelta(seconds=30), "30 seconds from now"),
#         (NOW + dt.timedelta(minutes=1, seconds=30), "a minute from now"),
#         (NOW + dt.timedelta(minutes=2), "2 minutes from now"),
#         (NOW + dt.timedelta(hours=1, minutes=30, seconds=30), "an hour from now"),
#         (NOW + dt.timedelta(hours=23, minutes=50, seconds=50), "23 hours from now"),
#         (NOW + dt.timedelta(days=1), "a day from now"),
#         (NOW + dt.timedelta(days=500), "1 year, 135 days from now"),
#         (NOW + dt.timedelta(days=365 * 2 + 35), "2 years from now"),
#         (NOW + dt.timedelta(days=10000), "27 years from now"),
#         (NOW - dt.timedelta(days=365 + 35), "1 year, 35 days ago"),
#         (30, "30 seconds ago"),
#         (NOW - dt.timedelta(days=365 * 2 + 65), "2 years ago"),
#         (NOW - dt.timedelta(days=365 + 4), "1 year, 4 days ago"),
#     ],
# )
# def test_date_time_no_months(
#     value: Union[dt.timedelta, int, dt.datetime], expected: str
# ) -> None:
#     """It returns relative time with no months."""
#     assert times.date_time(value, use_months=False) == expected


# @freezegun.freeze_time("2020-02-02")
# @pytest.mark.parametrize(
#     "date, expected",
#     [
#         (TODAY, "today"),
#         (TOMORROW, "tomorrow"),
#         (YESTERDAY, "yesterday"),
#         (dt.date(TODAY.year, 3, 5), "Mar 05"),
#     ],
# )
# def test_day(date: dt.date, expected: str) -> None:
#     """It returns natural day."""
#     assert times.day(date) == expected


# def test_day_formatting() -> None:
#     """It returns natural day with formatting."""
#     expected = "1982.06.27"
#     assert times.day(dt.date(1982, 6, 27), "%Y.%m.%d") == expected


# @freezegun.freeze_time("2020-02-02")
# @pytest.mark.parametrize(
#     "date, expected",
#     [
#         (TODAY, "today"),
#         (TOMORROW, "tomorrow"),
#         (YESTERDAY, "yesterday"),
#         (dt.date(TODAY.year, 3, 5), "Mar 05"),
#         (dt.date(1982, 6, 27), "Jun 27 1982"),
#         (dt.date(2019, 2, 2), "Feb 02 2019"),
#         (dt.date(2019, 3, 2), "Mar 02 2019"),
#         (dt.date(2019, 4, 2), "Apr 02 2019"),
#         (dt.date(2019, 5, 2), "May 02 2019"),
#         (dt.date(2019, 6, 2), "Jun 02 2019"),
#         (dt.date(2019, 7, 2), "Jul 02 2019"),
#         (dt.date(2019, 8, 2), "Aug 02 2019"),
#         (dt.date(2019, 9, 2), "Sep 02 2019"),
#         (dt.date(2019, 10, 2), "Oct 02"),
#         (dt.date(2019, 11, 2), "Nov 02"),
#         (dt.date(2019, 12, 2), "Dec 02"),
#         (dt.date(2020, 1, 2), "Jan 02"),
#         (dt.date(2020, 2, 2), "today"),
#         (dt.date(2020, 3, 2), "Mar 02"),
#         (dt.date(2020, 4, 2), "Apr 02"),
#         (dt.date(2020, 5, 2), "May 02"),
#         (dt.date(2020, 6, 2), "Jun 02"),
#         (dt.date(2020, 7, 2), "Jul 02"),
#         (dt.date(2020, 8, 2), "Aug 02 2020"),
#         (dt.date(2020, 9, 2), "Sep 02 2020"),
#         (dt.date(2020, 10, 2), "Oct 02 2020"),
#         (dt.date(2020, 11, 2), "Nov 02 2020"),
#         (dt.date(2020, 12, 2), "Dec 02 2020"),
#         (dt.date(2021, 1, 2), "Jan 02 2021"),
#         (dt.date(2021, 2, 2), "Feb 02 2021"),
#     ],
# )
# def test_date(date: dt.date, expected: str) -> None:
#     """It returns natural date."""
#     assert times.date(date) == expected


# def test_year() -> None:
#     """Tests year method."""
#     next_year = TODAY + ONE_YEAR
#     last_year = TODAY - ONE_YEAR

#     someyear = FakeDate(1988, 1, 1)
#     valerrtest = FakeDate(290149024, 2, 2)
#     overflowtest = FakeDate(120390192341, 2, 2)
#     test_list = [
#         TODAY,
#         next_year,
#         last_year,
#         "1955",
#         someyear,
#         None,
#         "Not a date at all.",
#         valerrtest,
#         overflowtest,
#     ]
#     result_list = [
#         "este ano",
#         "ano que vem",
#         "ano passado",
#         "1955",
#         "1988",
#         None,
#         "Not a date at all.",
#         valerrtest,
#         overflowtest,
#     ]
#     self.assert_many_results(
#         times.year, test_list, result_list
#     )


# @pytest.mark.parametrize(
#     "value, expected",
#     [
#         (dt.timedelta(seconds=1), "1 second"),
#         (1, "1 second"),
#         (2, "2 seconds"),
#         (60, "1 minute"),
#         (120, "2 minutes"),
#         (3600, "1 hour"),
#         (3600 * 2, "2 hours"),
#         (3600 * 24, "1 day"),
#         (3600 * 24 * 2, "2 days"),
#         (3600 * 24 * 365, "1 year"),
#         (3600 * 24 * 365 * 2, "2 years"),
#     ],
# )
# def test_precise_delta_min_seconds(
#     value: Union[dt.timedelta, int], expected: str
# ) -> None:
#     """It returns delta with minimum_unit default to second."""
#     assert times.precise_delta(value) == expected


# @pytest.mark.parametrize(
#     "value, min_unit, expected",
#     [
#         (dt.timedelta(microseconds=1), "microseconds", "1 microsecond"),
#         (dt.timedelta(microseconds=2), "microseconds", "2 microseconds"),
#         (dt.timedelta(microseconds=1000), "microseconds", "1 millisecond"),
#         (dt.timedelta(microseconds=2000), "microseconds", "2 milliseconds"),
#         (630, "minutes", "10.50 minutes"),
#     ],
# )
# def test_precise_delta_minimum_unit(
#     value: Union[dt.timedelta, int], min_unit: str, expected: str
# ) -> None:
#     """It returns delta considering minimum unit."""
#     assert times.precise_delta(value, minimum_unit=min_unit) == expected


# @pytest.mark.parametrize(
#     "value, min_unit, expected",
#     [
#         (
#             dt.timedelta(microseconds=1001),
#             "microseconds",
#             "1 millisecond and 1 microsecond",
#         ),
#         (
#             dt.timedelta(microseconds=2002),
#             "microseconds",
#             "2 milliseconds and 2 microseconds",
#         ),
#         (
#             dt.timedelta(seconds=1, microseconds=2),
#             "microseconds",
#             "1 second and 2 microseconds",
#         ),
#         (
#             dt.timedelta(hours=4, seconds=3, microseconds=2),
#             "microseconds",
#             "4 hours, 3 seconds and 2 microseconds",
#         ),
#         (
#             dt.timedelta(days=5, hours=4, seconds=3, microseconds=2),
#             "microseconds",
#             "5 days, 4 hours, 3 seconds and 2 microseconds",
#         ),
#         (
#             dt.timedelta(days=370, hours=4, seconds=3, microseconds=2),
#             "microseconds",
#             "1 year, 5 days, 4 hours, 3 seconds and 2 microseconds",
#         ),
#         (
#             dt.timedelta(days=370, microseconds=2),
#             "microseconds",
#             "1 year, 5 days and 2 microseconds",
#         ),
#         (
#             dt.timedelta(days=370, seconds=2),
#             "microseconds",
#             "1 year, 5 days and 2 seconds",
#         ),
#         (
#             dt.timedelta(seconds=0.01),
#             "minutes",
#             "0 minutes",
#         ),
#     ],
# )
# def test_precise_delta_combined_units(
#     value: Union[dt.timedelta, int], min_unit: str, expected: str
# ) -> None:
#     """It returns delta with combined units."""
#     assert times.precise_delta(value, minimum_unit=min_unit) == expected


@pytest.mark.parametrize(
    "value, min_unit, fmt, expected",
    [
        (
            dt.timedelta(microseconds=1001),
            "milliseconds",
            "%0.4f",
            "1.0010 milissegundos",
        ),
        (
            dt.timedelta(microseconds=2002),
            "milliseconds",
            "%0.4f",
            "2.0020 milissegundos",
        ),
        (
            dt.timedelta(microseconds=2002),
            "milliseconds",
            "%0.2f",
            "2.00 milissegundos",
        ),
        (
            dt.timedelta(seconds=1, microseconds=230000),
            "seconds",
            "%0.2f",
            "1.23 segundos",
        ),
        (
            dt.timedelta(hours=4, seconds=3, microseconds=200000),
            "seconds",
            "%0.2f",
            "4 horas e 3.20 segundos",
        ),
        (
            dt.timedelta(days=5, hours=4, seconds=30 * 60),
            "seconds",
            "%0.2f",
            "5 dias, 4 horas e 30 minutos",
        ),
        (
            dt.timedelta(days=5, hours=4, seconds=30 * 60),
            "hours",
            "%0.2f",
            "5 dias e 4.50 horas",
        ),
        (dt.timedelta(days=5, hours=4, seconds=30 * 60), "days", "%0.2f", "5.19 dias"),
        (dt.timedelta(days=120), "months", "%0.2f", "3.93 meses"),
        (dt.timedelta(days=183), "years", "%0.1f", "0.5 ano"),
    ],
)
def test_precise_delta_custom_format(
    activate_pt_br: MockerFixture,
    value: Union[dt.timedelta, int],
    min_unit: str,
    fmt: str,
    expected: str,
) -> None:
    """It returns custom formatted delta."""
    assert times.precise_delta(value, minimum_unit=min_unit, formatting=fmt) == expected
