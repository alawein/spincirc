---
type: canonical
source: none
sync: none
sla: none
authority: canonical
audience: [ai-agents, contributors]
last-verified: 2026-03-09
---

# SSOT — spincirc

**Version:** 1.0
**Last Updated:** 2026-03-03
**Status:** Active Research

---

## Purpose

SpinCirc — Spintronic device modeling using equivalent-circuit spin-transport methods. Implements drift-diffusion solvers with 4×4 conductance matrices, LLG/LLGS magnetization dynamics, and EDA-compatible compact models. Based on Alawein & Fariborzi, IEEE J-XCDC 2018.

## Current State

- Python research library: Active
- Drift-diffusion solvers: Implemented
- LLG/LLGS dynamics: Implemented
- EDA compact models: Implemented
- Based on published research (IEEE J-XCDC 2018)

## Structure

```
spincirc/
├── python/       # Python source
├── matlab/       # MATLAB models
├── CLAUDE.md     # Agent config
├── AGENTS.md     # Governance rules
└── SSOT.md       # This file
```

## Notes

- `pyproject.toml` contains only pytest and coverage tool config; this repo is not a distributed Python package.

## What's Next

- See CLAUDE.md for development commands

---

_Governed by: [AGENTS.md](AGENTS.md)_
See [CLAUDE.md](CLAUDE.md) | [AGENTS.md](AGENTS.md)
