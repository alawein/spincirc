SpinCirc documentation
======================

SpinCirc is a research repository for equivalent-circuit spin-transport work.
The supported Python distribution provides tools for processing MATLAB result
files; its public import namespace is ``spincirc``.

Status and verification
-----------------------

The Python tests, package build, installation smoke test, and documentation
build are automated in CI. MATLAB sources and Verilog-A models are retained as
**experimental and unverified** interfaces: this repository does not currently
provide executable CI evidence for either interface. They must not be treated
as release-validated simulators.

.. toctree::
   :maxdepth: 2
   :caption: Guides

   getting_started
   installation
   theory
   api
   architecture
   troubleshooting

Repository materials
--------------------

* ``matlab/`` contains MATLAB source and test assets, which require a suitable
  MATLAB environment and have not been verified by this project CI.
* ``verilogA/`` contains experimental, unverified Verilog-A models and a
  testbench. No compatible simulator invocation or expected-result check is
  included.
* ``python/spincirc/`` is the Python package source. Tests remain in
  ``python/tests/`` and are excluded from built distributions.

Citation
--------

The preferred scholarly reference is Alawein and Fariborzi, “Circuit Models
for Spintronic Devices Subject to Electric and Magnetic Fields,” IEEE JXCDC
(2018), DOI `10.1109/JXCDC.2018.2876456 <https://doi.org/10.1109/JXCDC.2018.2876456>`_.
The repository's ``CITATION.cff`` intentionally omits unverified page-range
metadata; consult the publisher record for bibliographic details.
