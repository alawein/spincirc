# SpinCirc

Status:      frozen
Category:    lab
Owner:       alawein
Visibility:  public
Purpose:     Spintronics circuit simulation and modeling research workspace.
Next action: continue

## Abstract

SpinCirc models spintronic devices with equivalent-circuit spin-transport methods, for circuit designers and device researchers who need compact models for circuit simulators rather than full micromagnetic simulation. `matlab/` holds drift-diffusion and LLG/LLGS solvers plus device models for spin valves, all-spin logic, and multiferroics; `python/` holds analysis, visualization, and ML parameter-extraction tools; `verilogA/models/` holds Verilog-A compact models (magnetic tunnel junction, four-terminal spin transport) for circuit simulators, work grounded in Alawein and Fariborzi, IEEE J-XCDC 2018. It does not replace full micromagnetic solvers (OOMMF, mumax3) for spatially resolved magnetization simulation.

## Status

- Lifecycle: frozen
- Verification date: 2026-08-28
- Scope: MATLAB core solvers, Python analysis tools, Verilog-A compact models

## Runtime requirements

- MATLAB R2024b+ with Signal Processing and Optimization toolboxes (`matlab/`)
- Python 3.9+ (dependencies pinned in `python/requirements.txt`; see Reproducibility)
- Verilog-A simulator (Spectre or equivalent) for `verilogA/models/`
- Docker optional via `docker-compose.yml` for containerized runs

## Reproducibility

Python:

```bash
python -m pip install -r python/requirements.txt
python -m pytest python/tests -q
```

MATLAB: requires MATLAB R2024b+ with Signal Processing and Optimization toolboxes;
not run for this README.

```matlab
addpath(genpath('matlab'));
runtests('matlab/tests');
```

Copy Verilog-A models to your simulator model directory before circuit-level runs.

## Datasets

- Material properties live in the repo material database modules (no external download required for bundled examples)
- Keep unpublished paper drafts, private benchmark data, and machine-local outputs
  out of public examples

## Architecture

```text
spincirc/
├── matlab/    # primary solvers (drift-diffusion, LLG/LLGS)
├── python/    # analysis, visualization, ML tooling
├── verilogA/  # compact EDA models
├── examples/  # runnable demos
└── docs/      # architecture, theory, API
```

Detail: [docs/architecture/topology.md](docs/architecture/topology.md) and [docs/architecture.md](docs/architecture.md).

## Docs map

- [docs/README.md](docs/README.md)
- [SSOT.md](SSOT.md)
- [LESSONS.md](LESSONS.md)
