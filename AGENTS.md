---
type: canonical
source: none
sync: none
sla: none
authority: canonical
audience: [agents, contributors, maintainers]
last_updated: 2026-09-06
last-verified: 2026-09-06
---

# AGENTS: SpinCirc

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

## Simplicity defaults

- Make the smallest change that satisfies the acceptance criteria.
- Prefer direct functions and plain data structures.
- No class when a function suffices. No framework for one implementation.
- No shared abstraction before real duplication exists.
- Prefer the standard library or an existing dependency.
- Avoid factories, registries, adapters, plugins, and config layers without multiple real consumers.
- Keep control flow direct. Use early returns when clearer. Keep errors explicit.
- Comments explain invariants, assumptions, and failure modes. Delete dead code instead of commenting it out.
- Keep pull requests single-purpose. Stop when tests and acceptance criteria pass. Do not rewrite adjacent working code without a stated need.

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
