Usage
=====

Humanization of lists:

.. code-block:: python

   human_readable.listing(["Cláudio", "Maria"], ",")
   "Cláudio, Maria"

   human_readable.listing(["Cláudio", "Maria"], ",", "e")
   "Cláudio e Maria"

   human_readable.listing(["Cláudio", "Maria", "José"], ";", "ou")
   "Cláudio; Maria ou José"
