.. _check_model:

=============
Check a model
=============

Two checker classes are provided in libCellML; the :code:`Validator` and the :code:`Analyser` classes.
These can be used to check the syntax and structure of your model is correct (validating), and to check that its mathematical representation is solvable (analysing). 

.. _validate_model:

Validate a model
================
The :code:`Validator` is the equivalent of a spelling checker: it can check that each item in a model has all of the information it needs, but it can't check whether it means what you intend it to.
Thus even if a model is valid, it could still be the equivalent of correctly-spelled nonsense.

.. include:: /resources/code_snippets/snippet_validate_model.rst

Once a model has been passed to a :code:`Validator` instance, the validator's internal logger will contain a list of any of the issues which have been encountered during the checking process. 
A model can be said to be valid - that is, conforming to the :cellml2:`CellML normative specification <>` - if the validator's logger contains no issues with a level of :code:`ERROR`.

For more information on how to use any of the classes which record issues, please see the :ref:`Get Issues<get_issues>` section below.

.. _get_issues:

Retrieve Issue items
====================

Selected libCellML classes contain a :code:`Logger` whose job it is to curate any issues encountered within the class, and return them to the user when asked.

.. container:: shortlist

    The classes are:

        - the :code:`Parser` class;
        - the :code:`Validator` class;
        - the :code:`Printer` class;
        - the :code:`Analyser` class;
        - the :code:`Importer` class; and
        - the :code:`Generator` class.

Individual issues can be retrieved from the parent class by their index, an integer between 0 and :code:`issueCount()-1`.
Each issue contains a severity level indicator, one of four levels (:code:`ERROR`, :code:`WARNING`, :code:`HINT`, or :code:`MESSAGE`):

.. container:: shortlist

  - :code:`ERROR` level indicates issues that must be resolved before the model is valid and runnable;
  - :code:`WARNING` level indicates a non-fatal issue, but one that may cause hidden or unintended consequences;
  - :code:`HINT` level indicates a commonly encountered valid-but-nonsense situation; and
  - :code:`MESSAGE` level is for your information but does not require action.

Issues can also be retrieved from subgroups based on their severity, as shown in the examples below.

.. tabs::

  .. tab:: C++

    .. literalinclude:: resources/code/check_model/check_model.cpp
      :language: cpp
      :start-after: // start CHECK_MODEL 1
      :end-before: // end CHECK_MODEL 1

  .. tab:: Python

    .. literalinclude:: resources/code/check_model/check_model.py
      :language: python
      :start-after: # start CHECK_MODEL 1
      :end-before: # end CHECK_MODEL 1

Each :code:`Issue` also contains the following attributes:

- A description: a brief statement about the problem and how it might be fixed;
- A reference heading: a chapter number pertaining to the formal :cellml2:`CellML 2.0 Specification <>` document, for issues related to formatting and specification;
- A URL: a web address at which more detailed information and examples pertaining to the issue are available;
- A cause: an :code:`enum` which reports the type of item responsible for the issue.
  This is one of the enums:

.. container:: shortlist

  - :code:`COMPONENT`,
  - :code:`CONNECTION`,
  - :code:`ENCAPSULATION`,
  - :code:`IMPORT`,
  - :code:`MAP_VARIABLES`,
  - :code:`MATHML`,
  - :code:`MODEL`,
  - :code:`RESET`,
  - :code:`RESET_VALUE`,
  - :code:`TEST_VALUE`,
  - :code:`UNDEFINED`,
  - :code:`UNIT`,
  - :code:`UNITS`,
  - :code:`VARIABLE`, and
  - :code:`XML`.

.. tabs::

  .. tab:: C++

    .. literalinclude:: resources/code/check_model/check_model.cpp
      :language: cpp
      :start-after: // start CHECK_MODEL 2
      :end-before: // end CHECK_MODEL 2

  .. tab:: Python

    .. literalinclude:: resources/code/check_model/check_model.py
      :language: python
      :start-after: # start CHECK_MODEL 2
      :end-before: # end CHECK_MODEL 2

Useful functions for dealing with Issues
========================================

.. include:: /resources/code_snippets/snippet_get_issues.rst

.. _analyse_model:

Analyse a Model item
====================

The :code:`Analyser` class takes an existing, valid :code:`Model` item, and checks it for mathematical sense.
This includes checking things like that all variables requiring initial values have them, that equations do not conflict with one another, and that any variables used in equations are actually defined in the model.

The three basic steps to model analysis are:

#. Creating an :code:`Analyser` item and passing in a :code:`Model` for analysis;
#. Checking for any :code:`Issues` raised; and
#. (optional: for code generation only) Retrieving a :code:`AnalysedModel` item to pass to a :code:`Generator`, if required.

.. include:: /resources/snippets/snippet_analyser_analyse.rst

Any issues or messages raised are stored within the class's logger.
More information about accessing :code:`Issue` items can be found on the :ref:`Common actions > Retrieve Issue items<get_issues>` page.

Use of the :code:`Analyser` class is a prerequisite for the :code:`Generator` class.
The generator makes use of the structures created during the analysis process, so takes a :code:`AnalyserModel` as an input.  

.. include:: /resources/snippets/snippet_analyser_output.rst

**TODO**
