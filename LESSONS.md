---
type: lessons
authority: observed
audience: [ai-agents, contributors, future-self]
last-updated: 2026-03-04
---

# LESSONS — SpinCirc

> Observed patterns only. Minimal initial entry — update as lessons accumulate.

## Patterns That Work

- **Equivalent-circuit formulation for spin transport**: The 4x4 conductance matrix / drift-diffusion approach (from Alawein & Fariborzi, IEEE J-XCDC 2018) provides EDA tool compatibility; maintaining Verilog-A compact models alongside MATLAB/Python implementations is a deliberate strength.
- **Validating MATLAB and Python implementations against each other**: Having two independent implementations of the same physics means discrepancies surface bugs; always cross-validate both before reporting results.

## Anti-Patterns

- **Treating Verilog-A models as secondary deliverables**: The circuit-compatible compact models are a key differentiator for EDA integration; they should be tested with the same rigor as the MATLAB/Python code.
- **LLG/LLGS solver without adaptive time-stepping**: Fixed time-step integration of magnetization dynamics is numerically fragile near switching events; use adaptive step control or validate fixed-step convergence explicitly.

## Pitfalls

- **MATLAB R2024b toolbox dependencies not available in all environments**: Signal Processing and Optimization toolboxes are required; document this clearly and provide Python fallbacks where feasible.
- **Drift-diffusion boundary conditions are easy to get wrong**: Incorrect boundary condition formulation at device interfaces produces physically wrong spin accumulation profiles that can look plausible; always verify against published device geometries from the paper.
