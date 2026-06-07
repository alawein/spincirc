---
type: canonical
owner: platform-engineering
last-reviewed: 2026-03-31
---

# Architecture Overview: spincirc

SpinCirc is a tri-language research library for spintronic device modeling.
The three language surfaces are intentionally separate: MATLAB owns the primary
numerical solvers, Python provides analysis and ML-adjacent tooling, and
Verilog-A delivers compact models for EDA circuit simulation.

## Components

- `matlab/`: drift-diffusion transport solver (4x4 conductance matrix), LLG/LLGS
  magnetization integrators (RK4, RK45, DP54, IMEX), and device-model classes
  (MTJ, nonlocal spin valve, all-spin logic, multiferroic).
- `python/`: data processing, visualization, and ML-adjacent tooling that
  operates on outputs produced by the MATLAB solvers.
- `verilogA/`: compact SPICE-compatible models for the MTJ and spin-valve
  devices, intended for use with Spectre or HSPICE.
- `examples/`: runnable demonstration scripts that exercise the MATLAB and
  Python surfaces.
- `docs/`: repo-local documentation including theory, API reference, and
  operational guides.

## Data Flow

1. MATLAB solvers run parametric sweeps or transient simulations and write
   numerical results (voltages, currents, magnetization trajectories) to
   `.mat` files or CSV outputs.
2. Python analysis scripts read those outputs for post-processing,
   statistical analysis, or ML model training.
3. Verilog-A compact models are loaded directly by an EDA simulator; they
   do not depend on the MATLAB or Python surfaces at runtime.

## Dependencies

- MATLAB R2024b or later, with Signal Processing and Optimization toolboxes.
- Python 3.9 or later; runtime dependencies listed in `python/requirements.txt`
  and declared in `pyproject.toml`.
- A SPICE-compatible EDA simulator (Spectre or HSPICE) for Verilog-A models.
- No shared runtime state exists between the language surfaces; each is
  independently executable.

## Constraints

- MATLAB is the authoritative numerical surface. Core transport and
  magnetodynamics solvers must not be silently rewritten into Python.
- Verilog-A models must remain compatible with the targeted EDA simulator
  workflow (standard Verilog-AMS / IEEE 1800).
- Validated benchmark and reference data are treated as immutable.
- The repo is currently frozen (research status). No production deployment
  pipeline exists.

