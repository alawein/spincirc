---
type: canonical
owner: platform-engineering
last-reviewed: 2026-03-31
---

# Troubleshooting: spincirc

This guide covers known failure modes and diagnostic steps for the MATLAB,
Python, and Verilog-A surfaces.

## Common Issues

**MATLAB path errors on startup**

If MATLAB reports that spincirc classes or functions are not found, the
`matlab/` tree has not been added to the path. Run:

```matlab
addpath(genpath('matlab'));
```

**Python import errors after install**

If `import spincirc` fails, confirm the package was installed in editable
mode from the repo root:

```bash
pip install -e .
```

Also confirm the active virtual environment matches the one where the package
was installed.

**Verilog-A model not found by simulator**

The `.va` files must be copied into the simulator's AHD library path or
explicitly referenced in the netlist. Consult the Spectre or HSPICE
documentation for model file path configuration.

**Test failures in MATLAB test suite**

Run the test suite with verbose output to isolate the failing test:

```matlab
runtests('matlab/tests', 'OutputDetail', 'Detailed');
```

Numerical tolerance failures typically indicate a platform-specific
floating-point difference; check whether the reference values in the
failing test match the expected device physics.

## Diagnostic Steps

1. Confirm the correct MATLAB version (R2024b or later) and that required
   toolboxes (Signal Processing, Optimization) are licensed and installed.
2. Confirm the Python virtual environment is active and dependencies match
   `python/requirements.txt`.
3. Run the Python test suite to isolate failures: `pytest python/tests/ -v`.
4. Run the MATLAB test suite: `runtests('matlab/tests')`.
5. Check the CHANGELOG for known regressions introduced in the current version.

## Known Failure Modes

- MATLAB solver divergence for extreme parameter combinations (very high spin
  polarization or very low damping) is a known numerical limitation, not a
  bug. Reduce the time step or apply physical parameter constraints.
- The Python ML tooling in `python/ml_tools/` is experimental and not covered
  by the main test suite. Treat its outputs as exploratory.

## FAQ

**Can I run SpinCirc without MATLAB?**

The Python and Verilog-A surfaces are independently usable, but the core
numerical solvers require MATLAB. There is no pure-Python port of the
transport and LLG solvers.

**Where do I report bugs or request features?**

Open an issue on the GitHub repository. See `CONTRIBUTING.md` for the
contribution process.

