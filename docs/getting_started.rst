Getting started
===============

The supported Python interface is the ``spincirc`` package for post-processing
simulation result files.

Install from a source checkout:

.. code-block:: bash

   python -m pip install .
   spincirc-process --help

Process a MATLAB result file:

.. code-block:: bash

   spincirc-process result.mat --report --output processed.h5 --format hdf5

The command reads a MATLAB ``.mat`` file and can emit a report or exported
processed data. See :doc:`installation` for separated test and docs dependencies.

MATLAB and Verilog-A
--------------------

The MATLAB and Verilog-A directories are experimental and unverified. This
repository does not currently provide automated executable evidence for a
MATLAB/Octave runtime or a Verilog-A simulator. Follow the source comments and
validate these interfaces in your own supported simulator environment.
