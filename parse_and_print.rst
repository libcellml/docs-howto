.. _serialise_model:

=============================
Parse and print CellML syntax
=============================


.. _parse_model:

Parse from a CellML format file
===============================

The following code will read a file called :code:`sine_comparison.cellml` and deserialise its contents into a :code:`Model` instance.

Note that both the :code:`Parser` class and its opposite number, the :code:`Printer` class, deal with strings rather than files.
You'll need to read the file into a string, and then use the string as input to the :code:`Parser` item.

.. include:: /resources/code_snippets/snippet_parse_model.rst

.. _print_model:

Print a model to CellML format
==============================

The :code:`Printer` class has the opposite functionality to the :code:`Parser` class.
It accepts an existing :code:`ModelPtr` and creates a :code:`string` which can be written to a file.
As with the :code:`Parser` and the :code:`Validator`, the :code:`Printer` also records a collection of :code:`Issue` items which can be accessed as shown below.

.. tabs::

  .. tab:: C++

    .. literalinclude:: resources/code/parse_and_print/parse_and_print.cpp
      :language: cpp

  .. tab:: Python

    .. literalinclude:: resources/code/parse_and_print/parse_and_print.py
      :language: python

Details of any issues that the printer encounters and records can be retrieved as described on the :ref:`Retrieve Issue items<get_issues>` page.
