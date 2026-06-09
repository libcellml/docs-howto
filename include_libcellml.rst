.. _include_libcellml:

=============================================
Include the libCellML library in your project
=============================================

If you've followed :installation:`the instructions for installing libCellML<build_from_source>` then the library is available for use as shown below.
Note that this doesn't invoke the libCellML namespace, so classes are accessed using the :code:`libcellml::` prefix.

.. literalinclude:: resources/code//include_libcellml/include_libcellml.cpp
  :language: cpp

In Python, the whole library can be imported at once, or classes can be imported individually as required.

.. literalinclude:: resources/code/include_libcellml/include_libcellml.py
  :language: python
