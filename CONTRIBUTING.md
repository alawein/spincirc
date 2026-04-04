---
type: canonical
source: _devkit/templates
sync: propagated
sla: none
---

# Contributing to spincirc

Spintronic device modeling using equivalent-circuit spin-transport methods.

This project follows the [alawein org contributing standards](https://github.com/alawein/alawein/blob/main/CONTRIBUTING.md).

## Getting Started

```bash
git clone https://github.com/alawein/spincirc.git
cd spincirc
pip install -e .
```

## Development Workflow

1. Branch off `main` using prefix: `feat/`, `fix/`, `docs/`, `chore/`, `test/`
2. Make your changes — keep PRs focused on a single concern
3. Run `pytest` to validate your changes before committing
4. Commit using [Conventional Commits](https://www.conventionalcommits.org/) — `type(scope): subject`
5. Open a Pull Request to `main`

## Code Standards

- MATLAB is primary language; Python tools are supplementary
- MATLAB files: `camelCase.m`; Python: `snake_case.py`; Verilog-A: `snake_case.va`
- Verilog-A models must be compatible with Spectre and HSPICE
- Do not modify validated benchmark results

## Pull Request Checklist

- [ ] CI passes (no failing checks)
- [ ] Tests added or updated for new functionality
- [ ] `black python/ && flake8 python/ && pytest` passes
- [ ] `CHANGELOG.md` updated under `[Unreleased]`
- [ ] No breaking changes without a version bump plan

## Reporting Issues

Open an issue on the [GitHub repository](https://github.com/alawein/spincirc/issues) with steps to reproduce and relevant context.

## License

By contributing, you agree that your contributions will be licensed under [MIT](LICENSE).
