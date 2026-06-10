.. _annotate_model:

================
Annotate a model
================

libCellML does not provide annotation functionality directly, but it can help with some of the things that you might need to know in order to implement your own.
Each annotation is attached to a unique ID locator which can be retrieved and edited, or created automatically if you haven't already set them yourself.
Since CellML is a subset of XML, any item may have an ID attribute, including operations within the MathML blocks, CellML entities, and CellML non-entity items (connections, encapsulations etc).
These ID attributes themselves must follow the specification rules: please see :cellml2:`1.2.5 XML ID attributes <specA2.html?issue=XML>` for details.

.. container:: nb

  At present, items within MathML blocks which have :code:`id` attributes are not retrieved or edited by the annotation class.
  Any editing or manipulation must be done external to libCellML.

.. contents::
    :local:

Annotation tools for entity items
=================================

Entity item types are:

- :code:`Model` items;
- :code:`Component` items;
- :code:`Variable` items;
- :code:`Units` items;
- :code:`Reset` items; and
- :code:`ImportSource` items.

The :code:`id` attribute for each of these entity types can be retrieved using the :code:`id()` function for the object, or set through its :code:`setId()` function.

.. tabs::

  .. tab:: C++

    .. literalinclude:: /resources/code/annotate_model/annotate_model.cpp
       :language: cpp
       :start-after: start - ANNOTATE_MODEL 1
       :end-before: end - ANNOTATE_MODEL 1

  .. tab:: Python

    .. literalinclude:: /resources/code/annotate_model/annotate_model.py
       :language: python
       :start-after: start - ANNOTATE_MODEL 1
       :end-before: end - ANNOTATE_MODEL 1

Annotation tools for other item types
=====================================

Connections and variable equivalence
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Items which specify the relationship between two entities (such as connections between components, and mappings between variables) are accessed and identified by the pair of entities.
Consider the simple example shown below.

.. code:: text

  model:
    ├─ component: name = "c1", id = "c1id"
    │   └ variable: name = "v1", id = "v1id" <╴╴╴┐
    └─ component: name = "c2", id = "c2id"     equivalent variables
        └ variable: name = "v2", id = "v2id" <╴╴╴┘

.. container:: toggle

  .. container:: header

    Show CellML syntax

  .. literalinclude:: /resources/code/annotate_model/annotate_model.cpp
      :language: xml
      :start-after: start - ANNOTATE_MODEL_XML 1
      :end-before: end - ANNOTATE_MODEL_XML 1

.. tabs::

  .. tab:: C++

    .. literalinclude:: /resources/code/annotate_model/annotate_model.cpp
       :language: cpp
       :start-after: start - ANNOTATE_MODEL 2
       :end-before: end - ANNOTATE_MODEL 2

  .. tab:: Python

    .. literalinclude:: /resources/code/annotate_model/annotate_model.py
       :language: python
       :start-after: start - ANNOTATE_MODEL 2
       :end-before: end - ANNOTATE_MODEL 2

Encapsulation and component references
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The model's encapsulation and the component references which it contains may have ID attributes too. 
These are accessed through the :code:`encapsulationId()` functions, as shown below.

.. code:: text

  model:
    └ encapsulation:
        └ component: grandparent
            └ component: parent
                └ component: child

.. container:: toggle

  .. container:: header

    Show CellML syntax

  .. literalinclude:: /resources/code/annotate_model/annotate_model.cpp
     :language: xml
     :start-after: start - ANNOTATE_MODEL_XML 2
     :end-before: end - ANNOTATE_MODEL_XML 2

There is only one encapsulation in a model, and its :code:`id` attribute is accessed using the very simple functions from the model instance.
The position of each component within that encapsulation structure is referenced using the same functions, but on the component instance instead.

.. tabs::

  .. tab:: C++

    .. literalinclude:: /resources/code/annotate_model/annotate_model.cpp
       :language: cpp
       :start-after: start - ANNOTATE_MODEL 3
       :end-before: end - ANNOTATE_MODEL 3

  .. tab:: Python

    .. literalinclude:: /resources/code/annotate_model/annotate_model.py
       :language: python
       :start-after: start - ANNOTATE_MODEL 3
       :end-before: end - ANNOTATE_MODEL 3

Unit item children; reset_value, test_value item children
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Some items are most readily accessed through their entity-type parents, these being:

- :code:`unit` items, a collection of which defines a :code:`Units` item; and
- :code:`test_value` and :code:`reset_value` children of :code:`Reset` items.

Unit children of :code:`Units` items can be accessed either through the streamlined ID-only functions :code:`unitId(index)` and :code:`setUnitId(index)`, or through the :code:`unitAttributes` family of functions.
Note that there are several overloads of the arguments for this function; please see the complete documentation on the :api:`Units functions API page <Units?fName=addUnit>`.

.. tabs::

  .. tab:: C++

    .. literalinclude:: /resources/code/annotate_model/annotate_model.cpp
       :language: cpp
       :start-after: start - ANNOTATE_MODEL 4
       :end-before: end - ANNOTATE_MODEL 4

  .. tab:: Python

    .. literalinclude:: /resources/code/annotate_model/annotate_model.py
       :language: python
       :start-after: start - ANNOTATE_MODEL 4
       :end-before: end - ANNOTATE_MODEL 4

Annotator ``Type`` and returned types
=====================================

+-------------------+-----------------------------------------------------------------------------------------------------+
| enumeration value | Object type in the "any" container.                                                                 |
+-------------------+-----------------------------------------------------------------------------------------------------+
| COMPONENT         | Pointer to a :code:`Component` with the given :code:`id`.                                           |
+-------------------+-----------------------------------------------------------------------------------------------------+
| COMPONENT_REF     | Pointer to a :code:`Component`, whose encapsulation :code:`component_ref` has the given :code:`id`. |
+-------------------+-----------------------------------------------------------------------------------------------------+
| CONNECTION        | :code:`VariablePair` containing pointers to two :code:`Variable` items which span the connection.   |
+-------------------+-----------------------------------------------------------------------------------------------------+
| ENCAPSULATION     | Pointer to the :code:`Model` item with the given :code:`id`.                                        |
+-------------------+-----------------------------------------------------------------------------------------------------+
| IMPORT            | Pointer to an :code:`ImportSource` item with the given :code:`id`.                                  |
+-------------------+-----------------------------------------------------------------------------------------------------+
| ISSUE             | Pointer to an :code:`Issue` item, created when something has gone wrong.                            |
+-------------------+-----------------------------------------------------------------------------------------------------+
| MAP_VARIABLES     | :code:`VariablePair` containing the two :code:`Variable` items connected by a variable              |
|                   | equivalence with the given :code:`id`.                                                              |
+-------------------+-----------------------------------------------------------------------------------------------------+
| MODEL             | Pointer to the :code:`Model` item with the given :code:`id`.                                        |
+-------------------+-----------------------------------------------------------------------------------------------------+
| RESET             | Pointer to the :code:`Reset` item with the given :code:`id`.                                        |
+-------------------+-----------------------------------------------------------------------------------------------------+
| RESET_VALUE       | Pointer to the parent :code:`Reset` item containing a reset value with the given :code:`id`.        |
+-------------------+-----------------------------------------------------------------------------------------------------+
| TEST_VALUE        | Pointer to the parent :code:`Reset` item containing a test value with the given :code:`id`.         |
+-------------------+-----------------------------------------------------------------------------------------------------+
| UNIT              | :code:`Unit` pair, when the first attribute is a :code:`Units` pointer to the parent of             |
|                   | the unit with the given :code:`id`, and the second attribute is the index within the                |
|                   | :code:`Units` item at which the unit can be found.                                                  |
+-------------------+-----------------------------------------------------------------------------------------------------+
| UNITS             | Pointer to a :code:`Units` item with the given :code:`id`.                                          |
+-------------------+-----------------------------------------------------------------------------------------------------+
| VARIABLE          | Pointer to a :code:`Variable` item with the given :code:`id`.                                       |
+-------------------+-----------------------------------------------------------------------------------------------------+

Useful snippets for annotation
==============================

.. include:: /resources/snippets/snippet_annotator_auto_ids.rst

.. include:: /resources/snippets/snippet_annotator_clear_all_ids.rst

.. include:: /resources/snippets/snippet_annotator_find_item_known_type.rst

.. include:: /resources/snippets/snippet_annotator_find_item_unknown_type.rst

.. include:: /resources/snippets/snippet_annotator_find_duplicate_ids.rst

.. include:: /resources/snippets/snippet_annotator_retrieve_duplicated_ids.rst
