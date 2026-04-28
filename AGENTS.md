---
type: canonical
source: none
sync: none
sla: none
authority: canonical
audience: [agents, contributors, maintainers]
last_updated: 2026-04-15
last-verified: 2026-04-15
---

# AGENTS — SpinCirc

## Workspace identity

SpinCirc is a tri-language research-library repo for spintronic device
modeling across MATLAB, Python, and Verilog-A.

## Directory structure

- `matlab/`: primary numerical solver surface
- `python/`: supplementary analysis and ML tooling
- `verilogA/`: compact-model surface for EDA flows
- `examples/`: runnable demos
- `docs/`: repo-local documentation

## Governance rules

1. MATLAB remains the primary numerical surface.
2. Keep Verilog-A models compatible with the targeted EDA simulator workflow.
3. Python tools should support the modeling workflow, not silently redefine it.
4. Numerical behavior changes need tests and explicit tolerance reasoning.
5. Comments should explain device, transport, or magnetodynamics assumptions.

## Code conventions

- Accurate docstrings and type hints where the language surface supports them
- Conventional commits only
- Update tests when public behavior changes

## Build and test commands

```bash
matlab -batch "runtests('matlab/tests')"
pytest python/tests/ -v --cov=python
black python/
flake8 python/
mypy python/
```
