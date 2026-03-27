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
type: normative
authority: canonical
audience: [agents, contributors, maintainers]
last-verified: 2026-03-09
---

# AGENTS — spincirc

> **Status: Normative.** Do not modify without maintainer review.

This repository is governed by clear engineering and documentation standards
aligned with the **Morphism Categorical Governance Framework** principles.

## Governance Source

| Authority | Location |
|-----------|----------|
| Root governance | [AGENTS.md](AGENTS.md) (this file) |
| Contributing guide | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Changelog | [CHANGELOG.md](CHANGELOG.md) |

## Repository Scope

MATLAB-primary library with Python tools and Verilog-A compact models for
spintronic device simulation. Covers drift-diffusion solvers, LLG/LLGS
magnetization dynamics, MTJs, spin valves, all-spin logic, and multiferroics.
Based on Alawein & Fariborzi, IEEE J-XCDC 2018.

## Directory Layout

| Directory | Purpose | Governance Level |
|-----------|---------|-----------------|
| `matlab/` | Core MATLAB solvers (transport, magnetodynamics, device models) | **Primary** -- all changes require tests |
| `python/` | Python data analysis and ML integration tools | **Supplementary** -- tests encouraged |
| `verilogA/` | EDA-compatible compact models for circuit simulation | **Primary** -- EDA compatibility required |
| `examples/` | Demo scripts | **Illustrative** -- must stay runnable |
| `tests/` | Test suite (MATLAB + Python) | **Required** -- never delete without replacement |
| `docker/` | Docker configuration | **Infrastructure** |

## Invariants (Must Always Hold)

<!-- STANDARD INVARIANTS — do not remove or weaken these -->

1. **Tests pass**: All tests must pass before merging to main
2. **Lint clean**: Linter must exit 0 on the primary source directories
3. **Imports work**: The package must be importable after install
4. **No secrets**: API keys or credentials must never appear in source
5. **Reproducibility**: Experiment and benchmark results must be deterministic (fixed seeds)
6. **README accurate**: README code examples must match actual API signatures

<!-- EXTENSION SLOT: Additional Invariants
     Add project-specific invariants here.
-->
7. **EDA compatibility**: Verilog-A models must be compatible with Spectre and HSPICE
8. **MATLAB primacy**: MATLAB is the primary language; Python tools are supplementary

## Agent Rules

When this repository is modified by an AI agent or automated tool:

<!-- STANDARD AGENT RULES — do not remove or weaken these -->

- **Read** `AGENTS.md` and `CONTRIBUTING.md` before making changes
- **Never** skip the test suite -- run tests before committing
- **Always** update `CHANGELOG.md` when changing public API or behavior
- **Always** keep docstrings and type hints accurate
- **Prefer** small, focused commits with conventional commit messages
- **Never** modify validated benchmark results or reference data

### Research-Specific Agent Rules

- **Data integrity**: Do not modify, rename, or delete files in immutable data
  directories (e.g., `data/`, `archive/`). Populate data directories via
  provided scripts; treat them as read-only afterward.
- **Numerical precision**: When comparing floating-point results, use tolerance-based
  comparisons. Do not tighten tolerances without verifying against known reference
  values. Document the precision requirements of any new numerical method.
- **Citation / attribution**: Update `CITATION.cff` for release-grade changes.
  Preserve author attribution in file headers. Reference the originating paper
  when implementing published algorithms.
- **Reproducibility**: All experiments, benchmarks, and simulations must be
  reproducible. Use fixed random seeds, pin dependency versions for published
  results, and record full parameter provenance for simulation outputs.

<!-- EXTENSION SLOT: Project-Specific Agent Rules
     Add rules unique to this project's domain.
-->
- MATLAB is the primary language -- Python tools are supplementary
- Verilog-A models must be compatible with standard EDA simulators (Spectre, HSPICE)
- Add tests for new features (MATLAB `runtests`, Python `pytest`)
- Do not modify validated benchmark results
- Update `CITATION.cff` for releases

## Naming Conventions

- **Modules**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **MATLAB files**: `camelCase.m`
- **MATLAB classes**: `PascalCase.m`
- **Verilog-A models**: `snake_case.va`

## Commit Message Format

```
type(scope): short description

feat(mtj): add temperature-dependent TMR model
fix(transport): correct conductance matrix symmetry
docs(readme): update device model catalog
test(llg): add precession angle edge case
refactor(python): extract parameter fitting utility
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `ci`, `chore`

## Dependency Policy

- **Core deps**: Keep minimal -- MATLAB toolboxes (Signal Processing, Optimization); Python: NumPy, SciPy, Matplotlib
- **Optional deps**: Visualization and ML tools as Python extras
- **Dev deps**: pytest, black, flake8, mypy -- no production code may import dev deps
- **Version pins**: Minimum versions only (no upper bounds unless proven necessary)

---

*Aligned with Morphism Systems governance principles.*

See [CLAUDE.md](CLAUDE.md) | [SSOT.md](SSOT.md)
