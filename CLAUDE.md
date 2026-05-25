---
type: canonical
source: none
sync: none
sla: none
authority: canonical
audience: [ai-agents, contributors]
last_updated: 2026-05-24
last-verified: 2026-05-24
---

# CLAUDE.md: SpinCirc

## Workspace identity

`spincirc` is a spintronic-device modeling workspace split across three
deliberate language surfaces: MATLAB for the primary solvers, Python for
analysis and auxiliary tooling, and Verilog-A for compact circuit models. That
split is part of the research contract and should stay visible.

Shared voice and agent contract:

- <https://github.com/alawein/alawein/blob/main/docs/style/VOICE.md>
- <https://github.com/alawein/alawein/blob/main/prompt-kits/AGENT.md>

## Directory structure

- `matlab/`: primary transport and magnetodynamics solvers
- `python/`: analysis, data processing, and ML-adjacent tooling
- `verilogA/`: compact models and test circuits
- `examples/`: runnable demos
- `docs/`: repo-local documentation

## Governance rules

1. MATLAB is the primary implementation surface. Do not casually rewrite core
   solvers into Python.
2. Verilog-A models must remain compatible with standard EDA simulators such as
   Spectre and HSPICE.
3. Treat validated benchmark or reference data as immutable.
4. Keep the tri-language split explicit in naming and documentation.
5. Reproducibility still applies: preserve seeds and test assumptions where
   stochastic workflows exist.

## Code conventions

- Comments should explain model assumptions, simulator constraints, or
  cross-language boundaries.
- Use MATLAB-style naming in `matlab/`, Python naming in `python/`, and
  explicit model naming in `verilogA/`.

## Build and test commands

```bash
matlab -batch "runtests('tests')"
pytest
black python/
flake8 python/
mypy python/
```
