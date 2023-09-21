How to for libCellML
====================

A collection of short how tos on using libCellML.

Running locally
---------------

To see the prepared documentation in a local browser when editing the documentation follow these steps:

1. Create a virtual environment::

    python -m venv venv-sphinx

2. Activate and install required packages::

    source venv-sphinx/bin/activate
    cd docs-howto
    pip install sphinx-hoverxref sphinx-tabs

3. Build documentation::

    sphinx-build . build

4. Serve documentation::

    cd build
    python -m http.server

5. View locally built documentation by visiting::

    http://localhost:8000
