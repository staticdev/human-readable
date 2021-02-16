Detailed usage
==============

Import the lib with:

.. code-block:: python

   import human_readable

File size humanization
----------------------

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
-----------------

**listing(items: List[str], separator: str, conjunction: str = "") -> str**

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
--------------------

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
----------------------------------

**fractional(value: Union[str, float]) -> str**

Return a human readable fractional number.

.. code-block:: python

   human_readable.fractional(1.5)
   "1 1/2"

   human_readable.fractional(0.3)
   "3/10"


Scientific notation
-------------------

**scientific_notation(value: Union[float, str], precision: int = 2) -> str**

Return number in string scientific notation z.wq x 10ⁿ.

.. code-block:: python

   human_readable.scientific_notation(1000)
   "1.00 x 10³"

You can also specify precision to it (default: 2):

.. code-block:: python

   human_readable.scientific_notation(5781651000, precision=4)
   "5.7817 x 10⁹"
