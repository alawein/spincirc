# SpinCirc

SpinCirc is a spintronic-device modeling workspace built across three explicit
language surfaces:

- MATLAB for the primary numerical solvers
- Python for analysis and auxiliary tooling
- Verilog-A for compact models in circuit-simulator flows

That split is the point. The repo is meant to make the transport,
magnetodynamics, and circuit-model boundaries visible instead of pretending one
language owns the whole problem.

## Core surfaces

- `matlab/`: primary transport and magnetodynamics solvers
- `python/`: analysis, data processing, and ML-adjacent tooling
- `verilogA/`: compact models and test circuits
- `examples/`: runnable demos
- `docs/`: repo-local documentation

## Device families

- magnetic tunnel junctions
- nonlocal spin valves
- all-spin logic
- multiferroic devices

## Quick start

### MATLAB

```matlab
addpath(genpath('matlab'));
```

### Python

```bash
python -m venv spincirc-env
source spincirc-env/bin/activate
pip install -r python/requirements.txt
pip install -e .
```

### Verilog-A

```bash
cp verilogA/models/*.va $SPECTRE_HOME/tools/spectre/etc/ahdl/
```

## Development

```matlab
runtests('matlab/tests');
```

```bash
pytest python/tests/ -v --cov=python
black python/
flake8 python/
mypy python/
```

## Documentation

Start with [docs/README.md](docs/README.md) for the architecture split and
release notes.
