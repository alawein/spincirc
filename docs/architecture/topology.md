---
type: canonical
last_updated: 2026-06-29
---

# Repository topology

Archetype: `python-research-package` with earned multi-language roots (fleet topology canon).

On-disk layout as of 2026-06-29. MATLAB owns primary solvers; Python and Verilog-A are separate surfaces.

## Tree

```text
spincirc/
├── matlab/                      # primary numerical solvers (authoritative surface)
│   ├── core/                    # drift-diffusion, LLG/LLGS integrators
│   ├── devices/                 # MTJ, spin valve, ASL, multiferroic models
│   ├── validation/              # benchmark and reference checks
│   └── tests/                   # MATLAB unit tests
├── python/                      # analysis, visualization, ML-adjacent tooling
│   ├── analysis/
│   ├── visualization/
│   ├── ml_tools/
│   └── tests/                   # pytest suite
├── verilogA/                    # compact EDA models
│   └── models/                  # Spectre/HSPICE-compatible Verilog-A
├── examples/                    # runnable demos per surface
├── docker/                      # containerized environment
├── scripts/                     # repo maintenance helpers
├── reports/                     # exported report artifacts
└── docs/                        # architecture, theory, API, operations
```

## Surfaces

| Path | Role |
|------|------|
| `matlab/` | Drift-diffusion transport, magnetization dynamics, device classes |
| `python/` | Post-processing and analysis on MATLAB outputs; no silent solver rewrites |
| `verilogA/models/` | Compact models loaded directly by EDA simulators |
| `examples/` | End-to-end demos tied to published figures where possible |
| `docker/` | Optional reproducible runs via `docker-compose.yml` |

## Rules

- MATLAB is the authoritative numerical surface for core transport and dynamics.
- No shared runtime state between language surfaces; each runs independently.
- Validated benchmark data is treated as immutable.

## Related docs

- [architecture.md](../architecture.md) for data flow between surfaces
