# SpinCirc

Status:      frozen
Category:    research
Owner:       alawein
Visibility:  private
Purpose:     Spintronics circuit simulation and modeling research workspace.
Next action: continue

## Abstract

SpinCirc models spintronic devices with equivalent-circuit spin-transport methods.
The framework couples drift-diffusion transport, magnetization dynamics (LLG/LLGS),
and EDA-ready compact models for MTJs, spin valves, all-spin logic, and multiferroic
devices. Work is grounded in Alawein and Fariborzi, IEEE J-XCDC 2018.

## Status

- Lifecycle: frozen
- Verification date: 2026-06-29
- Scope: MATLAB core solvers, Python analysis tools, Verilog-A compact models

## Runtime requirements

- MATLAB R2024b+ with Signal Processing and Optimization toolboxes (`matlab/`)
- Python 3.9+ with `pip install -r python/requirements.txt && pip install -e .`
- Verilog-A simulator (Spectre or equivalent) for `verilogA/models/`
- Docker optional via `docker-compose.yml` for containerized runs

## Reproducibility

MATLAB:

```matlab
addpath(genpath('matlab'));
runtests('matlab/tests');
```

Python:

```bash
python -m venv spincirc-env
source spincirc-env/bin/activate
pip install -r python/requirements.txt
pip install -e .
pytest python/tests/ -v --cov=python
```

Copy Verilog-A models to your simulator model directory before circuit-level runs.
Tie published figures to the demo scripts under `examples/` where possible.

## Datasets

- Material properties live in the repo material database modules (no external download required for bundled examples)
- Hanle and device benchmarks reference published experimental values cited in docs
- Keep unpublished paper drafts, private benchmark data, and machine-local outputs
  out of public examples

## Docs map

- [docs/README.md](docs/README.md)
- [SSOT.md](SSOT.md)
- [LESSONS.md](LESSONS.md)
