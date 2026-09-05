Installation
============

Python package
--------------

SpinCirc's supported Python package is installed from this repository:

.. code-block:: bash

   python -m pip install .

Optional dependency groups are deliberately separated:

.. code-block:: bash

   python -m pip install '.[test]'
   python -m pip install '.[docs]'

The requirements specify minimum versions; they are not a reproducible lockfile.
For a development checkout, run the Python suite with:

.. code-block:: bash

   python -m pytest python/tests -q

MATLAB and Verilog-A status
---------------------------

MATLAB sources and Verilog-A models are not installed by the Python package.
They are experimental and unverified in project CI. No supported automated
MATLAB/Octave invocation or Verilog-A simulator command is currently declared;
therefore the repository makes no execution claim for those interfaces.
