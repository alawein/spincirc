---
type: canonical
owner: platform-engineering
last-reviewed: 2026-03-31
---

# Deployment and Release: spincirc

SpinCirc is a research library, not a hosted service. There is no
production deployment pipeline. Distribution is through source checkout
and local environment setup.

## Deployment Process

SpinCirc is used by cloning the repository and installing language-surface
dependencies locally. There is no container registry, no cloud deployment
target, and no CI-driven publish step.

For the Python surface:

```bash
python -m venv spincirc-env
source spincirc-env/bin/activate  # Windows: spincirc-env\Scripts\activate
pip install -r python/requirements.txt
pip install -e .
```

For the MATLAB surface, add the `matlab/` directory tree to the MATLAB path:

```matlab
addpath(genpath('matlab'));
```

For Verilog-A models, copy `.va` files to your EDA simulator's model
directory as required by the simulator's documentation.

## Release Strategy

Releases follow semantic versioning. New versions are tagged on `main`
and documented in `CHANGELOG.md`. Because this is a research library in
frozen status, releases are infrequent and gated by the maintainer.

## Rollback Procedures

Rolling back a release means checking out the prior tag:

```bash
git checkout <previous-tag>
```

There is no stateful service or database to migrate; rollback is a
pure source operation.

## Environment Configuration

No secrets or environment variables are required for normal use. The MATLAB
and Python surfaces are self-contained given their respective dependency
installations. EDA simulator paths for Verilog-A models are configured
per-simulator and documented in the simulator's own environment setup.

