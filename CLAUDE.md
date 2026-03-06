---
type: guide
authority: canonical
audience: [ai-agents, contributors]
last-verified: 2026-03-03
---

# Claude AI Assistant Guide

## Repository Context

**Name:** SpinCirc  
**Type:** research-library  
**Purpose:** Spintronic device modeling using equivalent-circuit spin-transport methods. Implements drift-diffusion solvers with 4×4 conductance matrices, LLG/LLGS magnetization dynamics, and EDA-compatible compact models. Based on Alawein & Fariborzi, IEEE J-XCDC 2018.

## Tech Stack

- **Languages:** MATLAB R2024b+ (primary), Python 3.9+, Verilog-A (circuit models)
- **MATLAB toolboxes:** Signal Processing, Optimization
- **Python deps:** NumPy, SciPy, Matplotlib (optional: pytest, black, flake8, mypy)
- **Build (Python):** setuptools (`setup.py`)
- **Environment:** Docker available

## Key Files

- `README.md` — Main documentation
- `matlab/` — MATLAB core solvers (transport, magnetodynamics, device models)
- `python/` — Python data analysis and ML integration tools
- `verilogA/` — EDA-compatible compact models for circuit simulation
- `examples/` — Demo scripts
- `tests/` — Test suite (MATLAB `runtests` + Python `pytest`)
- `docker/` — Docker configuration
- `CITATION.cff` — Academic citation metadata

## Device Models

- **MTJs:** TMR calculation, bias dependence, switching dynamics
- **Nonlocal Spin Valves:** Hanle precession, temperature effects
- **All-Spin Logic (ASL):** Logic gates with process variation analysis
- **Multiferroic Devices:** Voltage-controlled magnetic anisotropy

## Development Guidelines

1. MATLAB is the primary implementation language — Python tools are supplementary
2. Verilog-A models must be compatible with standard EDA simulators (Spectre, HSPICE)
3. Add tests for new features (MATLAB `runtests`, Python `pytest`)
4. Use conventional commits
5. Update `CITATION.cff` for releases

## Common Tasks

### Running Tests
```bash
# Python
pytest
# MATLAB
matlab -batch "runtests('tests')"
```

### Building (Python)
```bash
python -m venv spincirc-env
source spincirc-env/bin/activate
pip install -e .
```

### Installing Verilog-A Models
```bash
cp verilogA/models/*.va $SPECTRE_HOME/tools/spectre/etc/ahdl/
```

## Architecture

Tri-language spintronic device simulation framework. MATLAB core provides numerical solvers for coupled spin-transport and magnetization dynamics equations. Python tools handle data analysis and ML-augmented parameter extraction. Verilog-A compact models enable integration with standard EDA circuit simulators for system-level spin-circuit co-design.

## Governance
See [AGENTS.md](AGENTS.md) for rules. See [SSOT.md](SSOT.md) for current state.
