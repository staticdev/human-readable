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
    SOME_YEAR = dt.date(1988, 11, 12)


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
    "value, expected",
    [
        (0, "um momento"),
        (dt.timedelta(seconds=1), "um segundo"),
        (30, "30 segundos"),
        (dt.timedelta(minutes=1, seconds=30), "um minuto"),
        (dt.timedelta(minutes=2), "2 minutos"),
        (dt.timedelta(hours=1, minutes=30, seconds=30), "uma hora"),
        (dt.timedelta(hours=23, minutes=50, seconds=50), "23 horas"),
        (dt.timedelta(days=1), "um dia"),
        (dt.timedelta(days=9), "9 dias"),
        (dt.timedelta(days=35), "um mês"),
        (dt.timedelta(days=65), "2 meses"),
        (dt.timedelta(days=365), "um ano"),
        (dt.timedelta(days=365 + 4), "1 ano e 4 dias"),
        (dt.timedelta(days=365 + 35), "1 ano e 1 mês"),
        (dt.timedelta(days=500), "1 ano e 4 meses"),
        (dt.timedelta(days=365 * 2 + 35), "2 anos"),
        (dt.timedelta(days=10000), "27 anos"),
    ],
)
def test_time_delta(
    activate_pt_br: MockerFixture, value: Union[dt.timedelta, int], expected: str
) -> None:
    """It returns delta in words."""
    assert times.time_delta(value) == expected


@freezegun.freeze_time("2020-02-02")
@pytest.mark.parametrize(
    "value, expected",
    [
        (NOW, "agora"),
        (NOW - dt.timedelta(seconds=1), "há um segundo"),
        (NOW - dt.timedelta(seconds=30), "há 30 segundos"),
        (NOW - dt.timedelta(minutes=1, seconds=30), "há um minuto"),
        (NOW - dt.timedelta(minutes=2), "há 2 minutos"),
        (NOW - dt.timedelta(hours=1, minutes=30, seconds=30), "há uma hora"),
        (NOW - dt.timedelta(hours=23, minutes=50, seconds=50), "há 23 horas"),
        (NOW - dt.timedelta(days=1), "há um dia"),
        (NOW - dt.timedelta(days=500), "há 1 ano e 4 meses"),
        (NOW - dt.timedelta(days=365 * 2 + 35), "há 2 anos"),
        (NOW + dt.timedelta(seconds=1), "em um segundo"),
        (NOW + dt.timedelta(seconds=30), "em 30 segundos"),
        (NOW + dt.timedelta(minutes=1, seconds=30), "em um minuto"),
        (NOW + dt.timedelta(minutes=2), "em 2 minutos"),
        (NOW + dt.timedelta(hours=1, minutes=30, seconds=30), "em uma hora"),
        (NOW + dt.timedelta(hours=23, minutes=50, seconds=50), "em 23 horas"),
        (NOW + dt.timedelta(days=1), "em um dia"),
        (NOW + dt.timedelta(days=500), "em 1 ano e 4 meses"),
        (NOW + dt.timedelta(days=365 * 2 + 35), "em 2 anos"),
        (NOW + dt.timedelta(days=10000), "em 27 anos"),
    ],
)
def test_date_time(
    activate_pt_br: MockerFixture,
    value: Union[dt.timedelta, int, dt.datetime],
    expected: str,
) -> None:
    """It returns relative time."""
    assert times.date_time(value) == expected


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
        (dt.time(23, 40, 30), "vinte para a meia-noite"),
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
        (SOME_YEAR, "1988"),
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
            "0.4f",
            "1.0010 milissegundos",
        ),
        (
            dt.timedelta(microseconds=2002),
            "milliseconds",
            "0.4f",
            "2.0020 milissegundos",
        ),
        (
            dt.timedelta(microseconds=2002),
            "milliseconds",
            "0.2f",
            "2.00 milissegundos",
        ),
        (
            dt.timedelta(seconds=1, microseconds=230000),
            "seconds",
            "0.2f",
            "1.23 segundos",
        ),
        (
            dt.timedelta(hours=4, seconds=3, microseconds=200000),
            "seconds",
            "0.2f",
            "4 horas e 3.20 segundos",
        ),
        (
            dt.timedelta(days=5, hours=4, seconds=30 * 60),
            "seconds",
            "0.2f",
            "5 dias, 4 horas e 30 minutos",
        ),
        (
            dt.timedelta(days=5, hours=4, seconds=30 * 60),
            "hours",
            "0.2f",
            "5 dias e 4.50 horas",
        ),
        (dt.timedelta(days=5, hours=4, seconds=30 * 60), "days", "0.2f", "5.19 dias"),
        (dt.timedelta(days=120), "months", "0.2f", "3.93 meses"),
        (dt.timedelta(days=183), "years", "0.1f", "0.5 ano"),
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
