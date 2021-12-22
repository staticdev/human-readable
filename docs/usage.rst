Usage
=====

.. include:: ../README.rst
   :start-after: basic-usage
   :end-before: end-basic-usage


Complete usage
--------------

Import the lib with:

.. code-block:: python

   import human_readable


Date and time humanization
~~~~~~~~~~~~~~~~~~~~~~~~~~

**time_of_day(hour: int) -> str**

Given current hour, returns time of the day.

.. code-block:: python

   human_readable.time_of_day(17)
   "afternoon"

**timing(time: dt.time, formal: bool = True) -> str**

Return human-readable time. Compares time values to present time returns representing readable of time with the given day period.

.. code-block:: python

   human_readable.timing(dt.time(6, 59, 0))
   "one minute to seven hours"

You can also specify formal=False, then it won't consider 24h time and instead tell the period of the day. Eg.:

.. code-block:: python

   human_readable.timing(dt.time(21, 0, 40), formal=False)
   "nine in the evening"

**time_delta(value: dt.timedelta | int | dt.datetime, use_months: bool = True, minimum_unit: str = "seconds", when: dt.datetime | None = None) -> str**

Return human-readable time difference. Given a timedelta or a number of seconds, return a natural representation of the amount of time elapsed. This is similar to ``date_time``, but does not add tense to the result. If ``use_months`` is True, then a number of months (based on 30.5 days) will be used for fuzziness between years. Eg.:

.. code-block:: python

   human_readable.time_delta(dt.timedelta(days=65))
   "2 months"


Args:
    value: A timedelta or a number of seconds.
    use_months: If `True`, then a number of months (based on 30.5 days) will be used for fuzziness between years.
    minimum_unit: The lowest unit that can be used. Options: "years", "months", "days", "hours", "minutes", "seconds", "milliseconds" or "microseconds".
    when: Point in time relative to which _value_ is interpreted.  Defaults to the current time in the local timezone.


Egs.:

.. code-block:: python

    human_readable.time_delta(dt.timedelta(hours=4, seconds=3, microseconds=2), minimum_unit="microseconds")
    "2 months"

    human_readable.time_delta(dt.timedelta(hours=4, seconds=30, microseconds=200), minimum_unit="microseconds", suppress=["hours"])
    "240 minutes, 30 seconds and 200 microseconds"

    human_readable.time_delta(dt.datetime.now(), when=dt.datetime.now())
    "a moment"

**date_time(value: dt.timedelta | int | dt.datetime, future: bool = False, use_months: bool = True, minimum_unit: str = "seconds", when: dt.datetime | None = None) -> str**

Return human-readable time. Given a datetime or a number of seconds, return a natural representation of that time in a resolution that makes sense. This is more or less compatible with Django's ``natural_time`` filter. ``future`` is ignored for datetimes, where the tense is always figured out based on the current time. If an integer is passed, the return value will be past tense by default, unless ``future`` is set to True.

Eg.:

.. code-block:: python

   human_readable.date_time(dt.datetime.now() - dt.timedelta(minutes=2))
   "2 minutes ago"

Args:
   value: time value.
   future: if false uses past tense. Defaults to False.
   use_months: if true return number of months. Defaults to True.
   minimum_unit: The lowest unit that can be used.
   when: Point in time relative to which _value_ is interpreted.  Defaults to the current time in the local timezone.

Specifing ``use_months=False`` you can supress that unit. Eg.:

.. code-block:: python

   human_readable.date_time(dt.datetime.now() - dt.timedelta(days=365 + 35), use_months=False)
   "1 year, 35 days ago"

For usage of ``minimum_unit`` and ``when`` just refer to ``time_delta()`` documentation above.

**day(date: dt.date, formatting: str = "%b %d") -> str**

Return human-readable day. For date values that are tomorrow, today or yesterday compared to present day returns representing string.

Eg.:

.. code-block:: python

   human_readable.day(dt.date.today() - dt.timedelta(days=1))
   "yesterday"

Otherwise, returns a string formatted according to ``formatting``.

Eg.:

.. code-block:: python

   human_readable.day(dt.date(1982, 6, 27), "%Y.%m.%d")
   "1982.06.27"

**date(date: dt.date) -> str**

Return human-readable date. Like ``day()``, but will append a year for dates that are a year ago or more.

Eg.:

.. code-block:: python

   human_readable.date(dt.date(2019, 7, 2))
   "Jul 02 2019"

**year(date: dt.date) -> str**

Return human-readable year. For date values that are last year, this year or next year compared to present year returns representing string. Otherwise, returns a string formatted according to the year.

Eg.:

.. code-block:: python

   human_readable.year(dt.date.today() + dt.timedelta(days=365))
   "next year"

   human_readable.year(dt.date(1988, 11, 12))
   "1988"


Precise delta humanization
~~~~~~~~~~~~~~~~~~~~~~~~~~

**precise_delta(value: dt.timedelta | int, minimum_unit: str = "seconds", suppress: list[str] | None = None, formatting: str = ".2f") -> str**

Return a precise representation of a timedelta.

Args:
   value: a time delta.
   minimum_unit: minimum unit.
   suppress: list of units to be suppressed.
   formatting: standard Python format.

Eg.:

.. code-block:: python

   delta = dt.timedelta(seconds=3633, days=2, microseconds=123000)
   human_readable.precise_delta(delta)
   "2 days, 1 hour and 33.12 seconds"

A custom `formatting` can be specified to control how the fractional part
is represented:

Eg.:

.. code-block:: python

   human_readable.precise_delta(delta, formatting=".4f")
   "2 days, 1 hour and 33.1230 seconds"

Instead, the `minimum_unit` can be changed to have a better resolution;
the function will still readjust the unit to use the greatest of the
units that does not lose precision.
For example setting microseconds but still representing the date with milliseconds:

Eg.:

.. code-block:: python

   human_readable.precise_delta(delta, minimum_unit="microseconds")
   "2 days, 1 hour, 33 seconds and 123 milliseconds"

If desired, some units can be suppressed: you will not see them represented and the
time of the other units will be adjusted to keep representing the same timedelta:

Eg.:

.. code-block:: python

   human_readable.precise_delta(delta, suppress=['days'])
   "49 hours and 33.12 seconds"

Note that microseconds precision is lost if the seconds and all
the units below are suppressed:

Eg.:

.. code-block:: python

   delta = dt.timedelta(seconds=90, microseconds=100)
   human_readable.precise_delta(delta, suppress=['seconds', 'milliseconds', 'microseconds'])
   "1.50 minutes"

If the delta is too small to be represented with the minimum unit,
a value of zero will be returned:

Egs.:

.. code-block:: python

   delta = dt.timedelta(seconds=1)
   human_readable.precise_delta(delta, minimum_unit="minutes")
   "0.02 minutes"

   delta = dt.timedelta(seconds=0.1)
   human_readable.precise_delta(delta, minimum_unit="minutes")
   "0 minutes"


File size humanization
~~~~~~~~~~~~~~~~~~~~~~

**file_size(value: int, binary: bool = False, gnu: bool = False, formatting: str = ".1f") -> str**

Return human-readable file size.

By default, decimal suffixes (kB, MB) are used.  Passing binary=true will use binary suffixes (KiB, MiB) are used and the base will be `2**10` instead of `10**3`.  If ``gnu`` is True, the binary argument is ignored and GNU-style (``ls -sh`` style) prefixes are used (K, M) with the `2**10` definition. Non-gnu modes are compatible with jinja2's ``filesizeformat`` filter.

.. code-block:: python

   human_readable.file_size(1000000)
   "1.0 MB"

   human_readable.file_size(1000000, binary=True)
   "976.6 KiB"

   human_readable.file_size(1000000, gnu=True)
   "976.6K"

You can also specify formatting in standard Python such as ".3f" (default: ".1f"):

.. code-block:: python

   human_readable.file_size(2900000, gnu=True, formatting=".3f")
   "2.766M"


List humanization
~~~~~~~~~~~~~~~~~

**listing(items: list[str], separator: str, conjunction: str = "") -> str**

Return human readable list separated by separator.

You can use listing with just a list of strings and a separator:

.. code-block:: python

   human_readable.listing(["Alpha", "Bravo"], ",")
   "Alpha, Bravo"

You can also specify an optional conjunction, so it is used between last and second last elements.

.. code-block:: python

   human_readable.listing(["Alpha", "Bravo"], ",", "and")
   "Alpha and Bravo"

   human_readable.listing(["Alpha", "Bravo", "Charlie"], ";", "or")
   "Alpha; Bravo or Charlie"


Numbers humanization
~~~~~~~~~~~~~~~~~~~~

**ordinal(value: Union[int, str]) -> str**

Convert an integer to its ordinal as a string.

.. code-block:: python

   human_readable.ordinal("1")
   "1st"

   human_readable.ordinal(111)
   "111th"

**int_comma(value: Union[str, float]) -> str**

Convert an integer to a string containing commas every three digits.

For example, 3000 becomes '3,000' and 45000 becomes '45,000'.  To maintain
some compatability with Django's int_comma, this function also accepts
floats.

.. code-block:: python

   human_readable.int_comma(12345)
   "12,345"

**int_word(value: float, formatting: str = ".1f") -> str**

Convert a large integer to a friendly text representation.

.. code-block:: python

   human_readable.int_word(123455913)
   "123.5 million"

   human_readable.int_word(12345591313)
   "12.3 billion"

You can also specify formatting in standard Python such as ".3f" (default: ".1f"):

.. code-block:: python

   human_readable.int_word(1230000, "0.2f")
   "1.23 million"

**ap_number(value: Union[float, str]) -> Union[str, float]**

For numbers 1-9, returns the number spelled out. Otherwise, returns the number.

This follows Associated Press style numbering:

.. code-block:: python

   human_readable.ap_number(4)
   "four"

   human_readable.ap_number(41)
   "41"


Floating point number humanization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**fractional(value: Union[str, float]) -> str**

Return a human readable fractional number.

.. code-block:: python

   human_readable.fractional(1.5)
   "1 1/2"

   human_readable.fractional(0.3)
   "3/10"


Scientific notation
~~~~~~~~~~~~~~~~~~~

**scientific_notation(value: Union[float, str], precision: int = 2) -> str**

Return number in string scientific notation z.wq x 10ⁿ.

.. code-block:: python

   human_readable.scientific_notation(1000)
   "1.00 x 10³"

You can also specify precision to it (default: 2):

.. code-block:: python

   human_readable.scientific_notation(5781651000, precision=4)
   "5.7817 x 10⁹"
