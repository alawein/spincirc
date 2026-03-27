---
type: canonical
source: none
sync: none
sla: none
---

<!-- Template: research-library v1.0.0 -->
<!-- Generated from _pkos governance templates. Do not edit the template sections -->
<!-- directly in consuming projects — update the template and re-sync instead.    -->
---
type: guide
authority: canonical
audience: [ai-agents, contributors]
last-verified: 2026-03-03
---

# CLAUDE.md — SpinCirc

## Repository Context

**Name:** SpinCirc
**Type:** research-library
**Purpose:** Spintronic device modeling using equivalent-circuit spin-transport methods.
Implements drift-diffusion solvers with 4x4 conductance matrices, LLG/LLGS magnetization
dynamics, and EDA-compatible compact models. Based on Alawein & Fariborzi, IEEE J-XCDC 2018.

---

## Tech Stack

- **Language:** MATLAB R2024b+ (primary), Python 3.9+, Verilog-A (circuit models)
- **Core deps:** MATLAB Signal Processing & Optimization toolboxes; Python: NumPy, SciPy, Matplotlib
- **Build:** setuptools (`setup.py`) for Python surface
- **Testing:** MATLAB `runtests`, Python `pytest`
- **Linting:** Python: black, flake8, mypy

<!-- EXTENSION SLOT: Toolchain
     Add project-specific toolchain details here (HPC tools, simulation
     engines, external solvers, GPU frameworks, etc.)
-->
- **EDA simulators:** Spectre, HSPICE (for Verilog-A compact model verification)
- **Docker:** Docker configuration available for reproducible environments

---

## Commands

### Setup

```bash
# Python
python -m venv spincirc-env
source spincirc-env/bin/activate
pip install -e .
# MATLAB
addpath(genpath('matlab'));
```

### Test

```bash
# Python
pytest
# MATLAB
matlab -batch "runtests('tests')"
```

### Lint / Format

```bash
black python/
flake8 python/
mypy python/
```

<!-- EXTENSION SLOT: Additional Commands
     Add project-specific command sections here (benchmarks, agents,
     SSOT, simulation workflows, HPC job submission, etc.)
-->

### Device Models

- **MTJs:** TMR calculation, bias dependence, switching dynamics
- **Nonlocal Spin Valves:** Hanle precession, temperature effects
- **All-Spin Logic (ASL):** Logic gates with process variation analysis
- **Multiferroic Devices:** Voltage-controlled magnetic anisotropy

### Installing Verilog-A Models

```bash
cp verilogA/models/*.va $SPECTRE_HOME/tools/spectre/etc/ahdl/
```

---

## Architecture Overview

Tri-language spintronic device simulation framework. MATLAB core provides numerical
solvers for coupled spin-transport and magnetization dynamics equations. Python tools
handle data analysis and ML-augmented parameter extraction. Verilog-A compact models
enable integration with standard EDA circuit simulators for system-level spin-circuit
co-design.

---

## Project Structure

```
spincirc/
├── matlab/                # Core MATLAB solvers (transport, magnetodynamics, device models)
├── python/                # Python data analysis and ML integration tools
├── verilogA/              # EDA-compatible compact models for circuit simulation
├── examples/              # Demo scripts
├── tests/                 # Test suite (MATLAB + Python)
├── docker/                # Docker configuration
└── CITATION.cff           # Academic citation metadata
```

---

## Key Configuration

| File | Purpose |
|------|---------|
| `pyproject.toml` | Build, deps, tool config |
| `AGENTS.md` | Governance invariants (normative) |
| `CITATION.cff` | Academic citation metadata |

---

## Important Notes / Known Quirks

<!-- Standard research library notes -->

**Deterministic seeds** -- All benchmark and experiment runs must use fixed seeds.
Reproducibility is a governance invariant. Never remove seed arguments from benchmark
or test code.

**Archive is read-only** -- If an `archive/` directory exists, it contains historical
data and papers. Never modify its contents.

**API stability** -- Breaking changes to the public API require a version bump and a
`CHANGELOG.md` entry.

**Pre-commit / linting** -- Run the project's format command before committing.

<!-- EXTENSION SLOT: Domain-Specific Notes
     Add project-specific quirks, numerical issues, data handling rules,
     dependency caveats, etc.
-->

**MATLAB is primary** -- MATLAB is the primary implementation language. Python tools are
supplementary for data analysis and ML integration.

**EDA compatibility** -- Verilog-A models must be compatible with standard EDA simulators
(Spectre, HSPICE). Test compatibility before releasing new model versions.

---

## Domain-Specific Rules

<!-- EXTENSION SLOT: Domain-Specific Rules
     Each project fills this section with rules unique to its research domain.
-->

- **MATLAB is the primary language**: Python tools are supplementary; do not rewrite MATLAB solvers in Python without explicit decision
- **Verilog-A models must be EDA-compatible**: All compact models must work with Spectre and HSPICE simulators
- **Multi-language naming**: MATLAB files use `camelCase.m`, Python modules use `snake_case.py`, Verilog-A models use `snake_case.va`
- **Do not modify validated benchmark results**: Device simulation reference data is immutable

---

## Data Integrity

<!-- EXTENSION SLOT: Data Integrity
     Define project-specific rules for data handling, reproducibility,
     and research artifact management.
-->

- **Device simulation reference data is immutable**: Validated benchmark results must not be modified
- **Verilog-A models must be tested against reference simulators**: New models require Spectre/HSPICE verification

---

## Governance

See [AGENTS.md](AGENTS.md) for rules. See [SSOT.md](SSOT.md) for current state.
