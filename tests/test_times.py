"""Tests for time humanizing."""
import datetime as dt

import pytest

import human_readable.times as times


TODAY = dt.date.today()
ONE_DAY_DELTA = dt.timedelta(days=1)
ONE_YEAR = dt.timedelta(days=365)


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
        # Watch: https://github.com/staticdev/humanizer-portugues/issues/137
        for arg, result in zip(test, results):  # type: ignore
            dtime, delta = times.date_and_delta(arg)
            assert_equal_datetime(dtime, result[0])
            assert_equal_timedelta(delta, result[1])


# def test_timing_formal() -> None:
#     """Tests timing method."""
#     meia_noite_meia = dt.time(0, 30, 0)
#     treze_um = dt.time(13, 1, 0)
#     dez_p_cinco = dt.time(4, 50, 10)
#     cinco_p_meiodia = dt.time(11, 55, 0)
#     vinteuma = dt.time(21, 0, 40)
#     overflowtest = FakeTime(120390192341, 2, 2)
#     test_list = [
#         meia_noite_meia,
#         treze_um,
#         dez_p_cinco,
#         cinco_p_meiodia,
#         vinteuma,
#         overflowtest,
#     ]
#     result_list = [
#         "zero hora e trinta minutos",
#         "treze horas e um minuto",
#         "dez minutos para cinco horas",
#         "cinco minutos para doze horas",
#         "vinte e uma horas",
#         overflowtest,
#     ]
#     self.assert_many_results(times.timing, test_list, result_list)


# def test_timing_informal() -> None:
#     """Tests timing method with formal=False."""
#     meia_noite_meia = dt.time(0, 30, 0)
#     treze_um = dt.time(13, 1, 0)
#     dez_p_cinco = dt.time(4, 50, 10)
#     cinco_p_meiodia = dt.time(11, 55, 0)
#     vinteuma = dt.time(21, 0, 40)
#     overflowtest = FakeTime(120390192341, 2, 2)
#     test_list = [
#         "Not a time at all.",
#         meia_noite_meia,
#         treze_um,
#         dez_p_cinco,
#         cinco_p_meiodia,
#         vinteuma,
#         overflowtest,
#     ]
#     result_list = [
#         "Not a time at all.",
#         "meia noite e meia",
#         "uma e um da tarde",
#         "dez para cinco da manhã",
#         "cinco para meio dia",
#         "nove da noite",
#         overflowtest,
#     ]
#     self.assert_many_results(
#         lambda d: times.timing(d, formal=False),
#         test_list,
#         result_list,
#     )


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
    """Test time_delta with no `use_months`."""
    assert times.time_delta(test_input, use_months=False) == expected


# @unittest.mock.patch("times._now")
# def test_time_delta_no_months(self, mocked: unittest.mock.Mock) -> None:
#     """Tests time_delta method with use_months=False."""
#     now = dt.datetime.now()
#     mocked.return_value = now
#     test_list = [
#         dt.timedelta(days=7),
#         dt.timedelta(days=31),
#         dt.timedelta(days=230),
#         dt.timedelta(days=366),
#         dt.timedelta(days=400),
#     ]
#     result_list = [
#         "7 dias",
#         "31 dias",
#         "230 dias",
#         "1 ano e 1 dia",
#         "1 ano e 35 dias",
#     ]
#     self.assert_many_results(
#         lambda d: times.time_delta(d, use_months=False),
#         test_list,
#         result_list,
#     )


# @unittest.mock.patch("times._now")
# def test_time_delta(self, mocked: unittest.mock.Mock) -> None:
#     """Tests time_delta method."""
#     now = dt.datetime.now()
#     mocked.return_value = now
#     test_list = [
#         0,
#         1,
#         30,
#         dt.timedelta(minutes=1, seconds=30),
#         dt.timedelta(minutes=2),
#         dt.timedelta(hours=1, minutes=30, seconds=30),
#         dt.timedelta(hours=23, minutes=50, seconds=50),
#         dt.timedelta(days=1),
#         dt.timedelta(days=500),
#         dt.timedelta(days=365 * 2 + 35),
#         dt.timedelta(seconds=1),
#         dt.timedelta(seconds=30),
#         dt.timedelta(minutes=1, seconds=30),
#         dt.timedelta(minutes=2),
#         dt.timedelta(hours=1, minutes=30, seconds=30),
#         dt.timedelta(hours=23, minutes=50, seconds=50),
#         dt.timedelta(days=1),
#         dt.timedelta(days=500),
#         dt.timedelta(days=365 * 2 + 35),
#         # regression tests for bugs in post-release humanize
#         dt.timedelta(days=10000),
#         dt.timedelta(days=365 + 35),
#         30,
#         dt.timedelta(days=365 * 2 + 65),
#         dt.timedelta(days=365 + 1),
#         dt.timedelta(days=365 + 4),
#         dt.timedelta(days=35),
#         dt.timedelta(days=65),
#         dt.timedelta(days=9),
#         dt.timedelta(days=365),
#         "NaN",
#     ]
#     result_list = [
#         "um momento",
#         "um segundo",
#         "30 segundos",
#         "um minuto",
#         "2 minutos",
#         "uma hora",
#         "23 horas",
#         "um dia",
#         "1 ano e 4 meses",
#         "2 anos",
#         "um segundo",
#         "30 segundos",
#         "um minuto",
#         "2 minutos",
#         "uma hora",
#         "23 horas",
#         "um dia",
#         "1 ano e 4 meses",
#         "2 anos",
#         "27 anos",
#         "1 ano e 1 mês",
#         "30 segundos",
#         "2 anos",
#         "1 ano e 1 dia",
#         "1 ano e 4 dias",
#         "um mês",
#         "2 meses",
#         "9 dias",
#         "um ano",
#         "NaN",
#     ]
#     self.assert_many_results(
#         times.time_delta, test_list, result_list
#     )


# @unittest.mock.patch("times._now")
# def test_date_time(self, mocked: unittest.mock.Mock) -> None:
#     """Tests date_time method."""
#     now = dt.datetime.now()
#     mocked.return_value = now
#     test_list = [
#         now,
#         now - dt.timedelta(seconds=1),
#         now - dt.timedelta(seconds=30),
#         now - dt.timedelta(minutes=1, seconds=30),
#         now - dt.timedelta(minutes=2),
#         now - dt.timedelta(hours=1, minutes=30, seconds=30),
#         now - dt.timedelta(hours=23, minutes=50, seconds=50),
#         now - dt.timedelta(days=1),
#         now - dt.timedelta(days=500),
#         now - dt.timedelta(days=365 * 2 + 35),
#         now + dt.timedelta(seconds=1),
#         now + dt.timedelta(seconds=30),
#         now + dt.timedelta(minutes=1, seconds=30),
#         now + dt.timedelta(minutes=2),
#         now + dt.timedelta(hours=1, minutes=30, seconds=30),
#         now + dt.timedelta(hours=23, minutes=50, seconds=50),
#         now + dt.timedelta(days=1),
#         now + dt.timedelta(days=500),
#         now + dt.timedelta(days=365 * 2 + 35),
#         # regression tests for bugs in post-release humanize
#         now + dt.timedelta(days=10000),
#         now - dt.timedelta(days=365 + 35),
#         30,
#         now - dt.timedelta(days=365 * 2 + 65),
#         now - dt.timedelta(days=365 + 4),
#         "NaN",
#     ]
#     result_list = [
#         "agora",
#         "há um segundo",
#         "há 30 segundos",
#         "há um minuto",
#         "há 2 minutos",
#         "há uma hora",
#         "há 23 horas",
#         "há um dia",
#         "há 1 ano e 4 meses",
#         "há 2 anos",
#         "em um segundo",
#         "em 30 segundos",
#         "em um minuto",
#         "em 2 minutos",
#         "em uma hora",
#         "em 23 horas",
#         "em um dia",
#         "em 1 ano e 4 meses",
#         "em 2 anos",
#         "em 27 anos",
#         "há 1 ano e 1 mês",
#         "há 30 segundos",
#         "há 2 anos",
#         "há 1 ano e 4 dias",
#         "NaN",
#     ]
#     self.assert_many_results(
#         times.date_time, test_list, result_list
#     )


# @unittest.mock.patch("times._now")
# def test_date_time_no_months(self, mocked: unittest.mock.Mock) -> None:
#     """Tests date_time method with use_months=False."""
#     now = dt.datetime.now()
#     mocked.return_value = now
#     test_list = [
#         now,
#         now - dt.timedelta(seconds=1),
#         now - dt.timedelta(seconds=30),
#         now - dt.timedelta(minutes=1, seconds=30),
#         now - dt.timedelta(minutes=2),
#         now - dt.timedelta(hours=1, minutes=30, seconds=30),
#         now - dt.timedelta(hours=23, minutes=50, seconds=50),
#         now - dt.timedelta(days=1),
#         now - dt.timedelta(days=17),
#         now - dt.timedelta(days=47),
#         now - dt.timedelta(days=500),
#         now - dt.timedelta(days=365 * 2 + 35),
#         now + dt.timedelta(seconds=1),
#         now + dt.timedelta(seconds=30),
#         now + dt.timedelta(minutes=1, seconds=30),
#         now + dt.timedelta(minutes=2),
#         now + dt.timedelta(hours=1, minutes=30, seconds=30),
#         now + dt.timedelta(hours=23, minutes=50, seconds=50),
#         now + dt.timedelta(days=1),
#         now + dt.timedelta(days=500),
#         now + dt.timedelta(days=365 * 2 + 35),
#         # regression tests for bugs in post-release humanize
#         now + dt.timedelta(days=10000),
#         now - dt.timedelta(days=365 + 35),
#         30,
#         now - dt.timedelta(days=365 * 2 + 65),
#         now - dt.timedelta(days=365 + 4),
#         "NaN",
#     ]
#     result_list = [
#         "agora",
#         "há um segundo",
#         "há 30 segundos",
#         "há um minuto",
#         "há 2 minutos",
#         "há uma hora",
#         "há 23 horas",
#         "há um dia",
#         "há 17 dias",
#         "há 47 dias",
#         "há 1 ano e 135 dias",
#         "há 2 anos",
#         "em um segundo",
#         "em 30 segundos",
#         "em um minuto",
#         "em 2 minutos",
#         "em uma hora",
#         "em 23 horas",
#         "em um dia",
#         "em 1 ano e 135 dias",
#         "em 2 anos",
#         "em 27 anos",
#         "há 1 ano e 35 dias",
#         "há 30 segundos",
#         "há 2 anos",
#         "há 1 ano e 4 dias",
#         "NaN",
#     ]
#     self.assert_many_results(
#         lambda d: times.date_time(d, use_months=False),
#         test_list,
#         result_list,
#     )


# def test_day() -> None:
#     """Tests day method."""
#     tomorrow = TODAY + ONE_DAY_DELTA
#     yesterday = TODAY - ONE_DAY_DELTA
#     if TODAY.month != 3:
#         someday = dt.date(TODAY.year, 3, 5)
#         someday_result = "5 de março"
#     else:
#         someday = dt.date(TODAY.year, 9, 5)
#         someday_result = "5 de setembro"
#     valerrtest = FakeDate(290149024, 2, 2)
#     overflowtest = FakeDate(120390192341, 2, 2)
#     test_list = [
#         TODAY,
#         tomorrow,
#         yesterday,
#         someday,
#         "02/26/1984",
#         None,
#         "Not a date at all.",
#         valerrtest,
#         overflowtest,
#     ]
#     result_list = [
#         "hoje",
#         "amanhã",
#         "ontem",
#         someday_result,
#         "02/26/1984",
#         None,
#         "Not a date at all.",
#         valerrtest,
#         overflowtest,
#     ]
#     self.assert_many_results(
#         times.day, test_list, result_list
#     )


# def test_date() -> None:
#     """Tests date method."""
#     tomorrow = TODAY + ONE_DAY_DELTA
#     yesterday = TODAY - ONE_DAY_DELTA

#     if TODAY.month != 3:
#         someday = dt.date(TODAY.year, 3, 5)
#         someday_result = "5 de março"
#     else:
#         someday = dt.date(TODAY.year, 9, 5)
#         someday_result = "5 de setembro"
#     valerrtest = FakeDate(290149024, 2, 2)
#     overflowtest = FakeDate(120390192341, 2, 2)

#     test_list = [
#         TODAY,
#         tomorrow,
#         yesterday,
#         someday,
#         dt.date(1982, 6, 27),
#         None,
#         "Not a date at all.",
#         valerrtest,
#         overflowtest,
#     ]
#     result_list = [
#         "hoje",
#         "amanhã",
#         "ontem",
#         someday_result,
#         "27 de junho de 1982",
#         None,
#         "Not a date at all.",
#         valerrtest,
#         overflowtest,
#     ]
#     self.assert_many_results(
#         times.date, test_list, result_list
#     )


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
