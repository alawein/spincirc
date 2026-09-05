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
- Python 3.9+ (minimum-version dependencies; see `requirements/`; see Reproducibility)
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


## Python package and verification status

The installable Python package uses the ``spincirc`` namespace. Install its
runtime tools with ``pip install .``; use ``pip install .[test]`` or
``pip install .[docs]`` for the test or documentation toolchains. Dependency
versions are minimum requirements, not lockfile pins.

``spincirc-process`` processes a MATLAB ``.mat`` result file; run
``spincirc-process --help`` for its command-line interface.

MATLAB sources and Verilog-A models are experimental and unverified in this
repository: no executable MATLAB/Octave or Verilog-A simulator evidence is
currently provided by CI. They are not release-validated interfaces.

## Citation

If you use SpinCirc, see ``CITATION.cff``. The scholarly reference is
[Alawein and Fariborzi (2018)](https://doi.org/10.1109/JXCDC.2018.2876456).
The page range is deliberately omitted from repository metadata because it has
not been confirmed against the publisher record.
