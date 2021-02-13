Usage
=====

Import the lib with:

.. code-block:: python

   import human_readable

File size humanization:

.. code-block:: python

   human_readable.natural_size(1000000)
   "1.0 MB"

   human_readable.natural_size(1000000, binary=True)
   "976.6 KiB"

   human_readable.natural_size(1000000, gnu=True)
   "976.6K"


List humanization:

.. code-block:: python

   human_readable.listing(["Alpha", "Bravo"], ",")
   "Alpha, Bravo"

   human_readable.listing(["Alpha", "Bravo"], ",", "and")
   "Alpha and Bravo"

   human_readable.listing(["Alpha", "Bravo", "Charlie"], ";", "or")
   "Alpha; Bravo or Charlie"
