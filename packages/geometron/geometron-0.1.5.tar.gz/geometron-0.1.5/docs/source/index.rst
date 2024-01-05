.. geometron documentation master file.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Documentation
^^^^^^^^^^^^^
.. raw:: html

    <div class="banner">
        <h2>A package to simplify mapping and survey reporting</h2>
        <a href="./examples/index.html"><img src="_static/banner_small.png" alt="geometron" width="100%"/></a>
    </div>

.. |GPLv3| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0


+----------------------+------------------------+
| License              | |GPLv3|                |
+----------------------+------------------------+

.. warning:: This version of the documentation is not yet up-to-date!


About
"""""

geometron is a python package providing basic tools for reporting geological and geophysical field work as maps or
layouts.

It provides ways do retrieve basemaps from web services, use them in matplotlib plots, add additional data such as
landmarks or stakes used in field work.

geometron is based on several package such as matplotlib, numpy, geopandas and pyvista.

Author
""""""
O. KAUFMANN  

Contributors
""""""""""""

* S. DEKENS
* T. MARTIN
* K. TSAKIRMPALOGLOU

.. toctree::
   :maxdepth: 1
   :caption: General Introduction
   
   Description<description.rst>


.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   Installation<installation.rst>
   First Steps<first_steps.rst>

.. toctree::
   :maxdepth: 1
   :caption: Examples
   
   Examples<auto_examples/index.rst>


.. toctree::
   :maxdepth: 1
   :caption: API Reference

   modules<modules.rst>
   uml<uml_diagrams.rst>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
