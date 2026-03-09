---
type: normative
authority: canonical
audience: [agents, contributors, maintainers]
last-verified: 2026-03-09
---

# AGENTS — spincirc

> Spintronic device modeling using equivalent-circuit spin-transport methods.
> Based on Alawein & Fariborzi, IEEE J-XCDC 2018.

## Repository Scope

MATLAB-primary library with Python tools and Verilog-A compact models for
spintronic device simulation. Covers drift-diffusion solvers, LLG/LLGS
magnetization dynamics, MTJs, spin valves, all-spin logic, and multiferroics.

## Key Directories

| Directory | Purpose |
|-----------|---------|
| `matlab/` | Core MATLAB solvers (transport, magnetodynamics, device models) |
| `python/` | Python data analysis and ML integration tools |
| `verilogA/` | EDA-compatible compact models for circuit simulation |
| `examples/` | Demo scripts |
| `tests/` | Test suite (MATLAB + Python) |
| `docker/` | Docker configuration |

## Commands

- MATLAB: `addpath(genpath('matlab'));` then run scripts
- Python: `pip install -e .` and `pytest`
- MATLAB tests: `matlab -batch "runtests('tests')"`
- Python tests: `pytest`

## Agent Rules

- Read this file before making changes
- MATLAB is the primary language -- Python tools are supplementary
- Verilog-A models must be compatible with standard EDA simulators (Spectre, HSPICE)
- Add tests for new features (MATLAB `runtests`, Python `pytest`)
- Do not modify validated benchmark results
- Update `CITATION.cff` for releases
- Use conventional commit messages: `feat(scope):`, `fix(scope):`, etc.

## Naming Conventions

- MATLAB files: `camelCase.m`
- MATLAB classes: `PascalCase.m`
- Python modules: `snake_case.py`
- Python classes: `PascalCase`
- Verilog-A models: `snake_case.va`
- Constants: `UPPER_SNAKE_CASE`

See [CLAUDE.md](CLAUDE.md) | [SSOT.md](SSOT.md)