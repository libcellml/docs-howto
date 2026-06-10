.. _view_model:

================================
View the contents of a ``Model``
================================

.. contents::
    :local:
    
About viewing models
====================
All CellML entities exist in a hierarchical structure as shown below.
In some circumstances additional links are made between items (equivalent variables, for example), but on the whole it follows a basic tree structure.

.. code:: text

  Model
    │
    ├─ Units item(s)
    │   └─ Unit item(s)
    │
    └─ Component item(s)
        │
        ├─ Variable item(s)
        │
        ├─ Reset item(s)
        │   ├─ ResetValue item
        │   └─ TestValue item
        │
        ├─ Math item
        │
        └─ Child Component item(s)
             │
             └─ Grandchild Component item(s)

Within the structure each item has two parts:

- A set of *attributes* specific to itself.
  Some of these attribute exist for many items (for example, the :code:`name` attribute), and others are specific to the item type (for example, the :code:`initialValue` attribute on a :code:`Variable` item).
- A set of *collections* which this - the parent item - curates.
  For example, the collection of :code:`Variable` items owned by a parent :code:`Component`.

View attributes of an item
--------------------------
Retrieving the value of an item's attribute is simple, and follows the same general pattern throughout libCellML.
Get the attribute :code:`xyz` using the camelCase function :code:`xyx()` without arguments.

For example:

.. tabs::

  .. tab:: C++

    .. literalinclude:: resources/code/view_model/view_model.cpp
      :language: cpp
      :start-after: // start - VIEW_MODEL 1
      :end-before: // end - VIEW_MODEL 1

  .. tab:: Python

    .. literalinclude:: resources/code/view_model/view_model.py
      :language: python
      :start-after: # start - VIEW_MODEL 1
      :end-before: # end - VIEW_MODEL 1

Note that the return value's type will vary depending on the function.
For example, a :code:`Variable` item pointer is returned as the :code:`testVariable()` attribute value for a :code:`Reset` item:


.. tabs::

  .. tab:: C++

    .. literalinclude:: resources/code/view_model/view_model.cpp
      :language: cpp
      :start-after: // start - VIEW_MODEL 2
      :end-before: // end - VIEW_MODEL 2

  .. tab:: Python

    .. literalinclude:: resources/code/view_model/view_model.py
      :language: python
      :start-after: # start - VIEW_MODEL 2
      :end-before: # end - VIEW_MODEL 2

View collections owned by an item
---------------------------------
In order to access items within a collection use the same general format as above, but with an indicator (name or index) of the child item to be retrieved from the collection.
In other words, get the child item of type :code:`xyz` using the camelCase function :code:`xyx(myIndex)` or :code:`xyz(myName)`.

.. container:: nb

    Before accessing a collection item using an index, you can use the :code:`xyzCount()` function to return the number of items in the collection.

The following example shows how all variables in a component can be listed.

.. tabs::

  .. tab:: C++

    .. literalinclude:: resources/code/view_model/view_model.cpp
      :language: cpp
      :start-after: // start - VIEW_MODEL 3
      :end-before: // end - VIEW_MODEL 3

  .. tab:: Python

    .. literalinclude:: resources/code/view_model/view_model.py
      :language: python
      :start-after: # start - VIEW_MODEL 3
      :end-before: # end - VIEW_MODEL 3

Some gotchas
------------
The ownership of some collections can be a little counter-intuitive.
One example is that :code:`Units` items are referenced by :code:`Variable` items, but are owned by the :code:`Model`; this is so that units can be reused across more than one component.
Another example involving encapsulation and :code:`Component` item ownership is shown below.

Consider the following model:

.. code::

  model: Grandfather
    component: Uncle
    component: Mother
      component: Daughter
      component: Son

The raw CellML syntax stores each component individually as children of the model, and separately stores the encapsulation structure of the nested components.

.. container:: toggle

  .. container:: header

    See CellML syntax

  .. code-block:: xml

    <model>

      <!-- The components are listed individually as children of the model block. -->
      <component name="Uncle"/>
      <component name="Mother"/>
      <component name="Daughter"/>
      <component name="Son"/>

      <!-- The encapsulation structure is stored separate from the components. -->
      <encapsulation>
        <component_ref component="Mother">
          <component_ref component="Daughter"/>
          <component_ref component="Son"/>
        </component_ref>
      </encapsulation>
    </model>


In libCellML, the encapsulation structure is embedded in the ownership of the components, so that one component can be a parent of another.
This can be confusing if the simple :code:`componentCount()` function on a model is called naively, as shown below.

.. tabs::

  .. tab:: C++

    .. literalinclude:: resources/code/view_model/view_model.cpp
      :language: cpp
      :start-after: // start - VIEW_MODEL 4
      :end-before: // end - VIEW_MODEL 4

  .. tab:: Python

    .. literalinclude:: resources/code/view_model/view_model.py
      :language: python
      :start-after: # start - VIEW_MODEL 4
      :end-before: # end - VIEW_MODEL 4

Useful snippets for viewing a model
===================================

Some useful snippets for viewing parts of your model are shown below.

.. include:: /resources/snippets/snippet_print_units.rst

.. include:: /resources/snippets/snippet_edit_mathml.rst

.. include:: /resources/snippets/snippet_print_encapsulation.rst

.. include:: /resources/snippets/snippet_print_equivalent_variables.rst
