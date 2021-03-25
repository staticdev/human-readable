Human Readable
==============

|PyPI| |Python Version| |License|

|Read the Docs| |Tests| |Codecov|

|pre-commit| |Black|

.. |PyPI| image:: https://img.shields.io/pypi/v/human-readable.svg
   :target: https://pypi.org/project/human-readable/
   :alt: PyPI
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/human-readable
   :target: https://pypi.org/project/human-readable
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/human-readable
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/human-readable/latest.svg?label=Read%20the%20Docs
   :target: https://human-readable.readthedocs.io/
   :alt: Read the documentation at https://human-readable.readthedocs.io/
.. |Tests| image:: https://github.com/staticdev/human-readable/workflows/Tests/badge.svg
   :target: https://github.com/staticdev/human-readable/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/staticdev/human-readable/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/staticdev/human-readable
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black


Features
--------

* File size humanization.
* List humanization.
* Numbers humanization.
* Time and dates humanization.
* Internacionalization (i18n) to 20+ locales:

  * Abbreviated English (en_ABBR)
  * Brazilian Portuguese (pt_BR)
  * Dutch (nl_NL)
  * Finnish (fi_FI)
  * French (fr_FR)
  * German (de_DE)
  * Indonesian (id_ID)
  * Italian (it_IT)
  * Japanese (ja_JP)
  * Korean (ko_KR)
  * Persian (fa_IR)
  * Polish (pl_PL)
  * Portugal Portuguese (pt_PT)
  * Russian (ru_RU)
  * Simplified Chinese (zh_CN)
  * Slovak (sk_SK)
  * Spanish (es_ES)
  * Taiwan Chinese (zh_TW)
  * Turkish (tr_TR)
  * Ukrainian (uk_UA)
  * Vietnamese (vi_VI)


Requirements
------------

* It works in Python 3.7+.


Installation
------------

You can install *Human Readable* via pip_ from PyPI_:

.. code:: console

   $ pip install human-readable


.. basic-usage

Basic usage
-----------

Import the lib with:

.. code-block:: python

   import human_readable


Date and time humanization examples:

.. code-block:: python

   human_readable.time_of_day(17)
   "afternoon"

   import datetime as dt
   human_readable.timing(dt.time(6, 59, 0))
   "one minute to seven hours"

   human_readable.timing(dt.time(21, 0, 40), formal=False)
   "nine in the evening"

   human_readable.time_delta(dt.timedelta(days=65))
   "2 months"

   human_readable.date_time(dt.datetime.now() - dt.timedelta(minutes=2))
   "2 minutes ago"

   human_readable.day(dt.date.today() - dt.timedelta(days=1))
   "yesterday"

   human_readable.date(dt.date(2019, 7, 2))
   "Jul 02 2019"

   human_readable.year(dt.date.today() + dt.timedelta(days=365))
   "next year"


Precise time delta examples:

.. code-block:: python

   import datetime as dt
   delta = dt.timedelta(seconds=3633, days=2, microseconds=123000)
   human_readable.precise_delta(delta)
   "2 days, 1 hour and 33.12 seconds"

   human_readable.precise_delta(delta, minimum_unit="microseconds")
   "2 days, 1 hour, 33 seconds and 123 milliseconds"

   human_readable.precise_delta(delta, suppress=["days"], format="0.4f")
   "49 hours and 33.1230 seconds"


File size humanization examples:

.. code-block:: python

   human_readable.file_size(1000000)
   "1.0 MB"

   human_readable.file_size(1000000, binary=True)
   "976.6 KiB"

   human_readable.file_size(1000000, gnu=True)
   "976.6K"


Lists humanization examples:

.. code-block:: python

   human_readable.listing(["Alpha", "Bravo"], ",")
   "Alpha, Bravo"

   human_readable.listing(["Alpha", "Bravo", "Charlie"], ";", "or")
   "Alpha; Bravo or Charlie"


Numbers humanization examples:

.. code-block:: python

   human_readable.int_comma(12345)
   "12,345"

   human_readable.int_word(123455913)
   "123.5 million"

   human_readable.int_word(12345591313)
   "12.3 billion"

   human_readable.ap_number(4)
   "four"

   human_readable.ap_number(41)
   "41"


Floating point number humanization examples:

.. code-block:: python

   human_readable.fractional(1.5)
   "1 1/2"

   human_readable.fractional(0.3)
   "3/10"


Scientific notation examples:

.. code-block:: python

   human_readable.scientific_notation(1000)
   "1.00 x 10³"

   human_readable.scientific_notation(5781651000, precision=4)
   "5.7817 x 10⁹"

.. end-basic-usage

Complete instructions can be found at `human-readable.readthedocs.io`_.


Localization
------------

How to change locale at runtime:

.. code-block:: python

   import datetime as dt
   human_readable.date_time(dt.timedelta(seconds=3))
   '3 seconds ago'

   _t = human_readable.i18n.activate("ru_RU")
   human_readable.date_time(dt.timedelta(seconds=3))
   '3 секунды назад'

   human_readable.i18n.deactivate()
   human_readable.date_time(dt.timedelta(seconds=3))
   '3 seconds ago'


You can pass additional parameter `path` to `activate` to specify a path to search
locales in.

.. code-block:: python

   human_readable.i18n.activate("xx_XX")
   ...
   FileNotFoundError: [Errno 2] No translation file found for domain: 'human_readable'
   human_readable.i18n.activate("pt_BR", path="path/to/my/portuguese/translation/")
   <gettext.GNUTranslations instance ...>

You can see how to add a new locale on the `Contributor Guide`_.

A special locale, `en_ABBR`, renderes abbreviated versions of output:

.. code-block:: python

    human_readable.date_time(datetime.timedelta(seconds=3))
    3 seconds ago

    human_readable.int_word(12345591313)
    12.3 billion

    human_readable.date_time(datetime.timedelta(seconds=86400*476))
    1 year, 3 months ago

    human_readable.i18n.activate('en_ABBR')
    human_readable.date_time(datetime.timedelta(seconds=3))
    3s

    human_readable.int_word(12345591313)
    12.3 B

    human_readable.date_time(datetime.timedelta(seconds=86400*476))
    1y 3M


Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the MIT_ license,
*Human Readable* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits
-------

This lib is based on original humanize_ with some added features such as listing, improved naming, documentation, functional tests, type-annotations, bug fixes and better localization.

This project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.


.. _@cjolowicz: https://github.com/cjolowicz
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _MIT: http://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/
.. _humanize: https://github.com/jmoiron/humanize
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/staticdev/human-readable/issues
.. _pip: https://pip.pypa.io/
.. _human-readable.readthedocs.io: https://human-readable.readthedocs.io
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
