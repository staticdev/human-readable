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
    LAST_YEAR = TODAY - 365 * ONE_DAY_DELTA
    NEXT_YEAR = TODAY + 365 * ONE_DAY_DELTA


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


@freezegun.freeze_time("2020-02-02")
@pytest.mark.parametrize(
    "date, expected",
    [
        (TODAY, "este ano"),
        (NEXT_YEAR, "ano que vem"),
        (LAST_YEAR, "ano passado"),
        (FakeDate(1988, 1, 1), "1988"),
    ],
)
def test_year(activate_pt_br: MockerFixture, date: dt.date, expected: str) -> None:
    """Tests year method."""
    result = times.year(date)

    assert result == expected


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
