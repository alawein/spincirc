# SpinCirc

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![MATLAB](https://img.shields.io/badge/MATLAB-R2024b+-orange.svg)](https://www.mathworks.com/products/matlab.html)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Verilog-A](https://img.shields.io/badge/VerilogA-IEEE1800-green.svg)](https://en.wikipedia.org/wiki/Verilog-AMS)

Computational framework for spintronic device modeling using equivalent-circuit spin-transport methods. Based on Alawein & Fariborzi, IEEE J-XCDC 2018.

## Features

- **Spin Transport** -- Drift-diffusion solver with 4x4 conductance matrix
- **Magnetization Dynamics** -- LLG/LLGS integration with thermal noise
- **Device Models** -- MTJs, spin valves, all-spin logic, multiferroic devices
- **Circuit Integration** -- EDA-compatible compact models
- **Material Database** -- Properties for common spintronic materials

## Implementation

- **MATLAB Core** -- Numerical solvers for coupled transport-magnetodynamics
- **Python Tools** -- Data analysis and ML integration
- **Verilog-A Models** -- Compact models for circuit simulation
- **Validation** -- Benchmarks against published experiments

## Device Models

- **Magnetic Tunnel Junctions (MTJs)** -- TMR calculation, bias dependence, switching
- **Nonlocal Spin Valves** -- Hanle precession measurements, temperature effects
- **All-Spin Logic (ASL)** -- Logic gates with process variation analysis
- **Multiferroic Devices** -- Voltage-controlled magnetic anisotropy

## Installation

### MATLAB
Requires R2024b+ with Signal Processing and Optimization toolboxes.
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

### Verilog-A Models
Copy `.va` files to your simulator's model directory:
```bash
cp verilogA/models/*.va $SPECTRE_HOME/tools/spectre/etc/ahdl/
```

## Usage

```matlab
% Nonlocal spin valve simulation
device = NonlocalSpinValve();
device.setGeometry(2e-6, 100e-9, 10e-9);
device.setMaterials('NiFe', 'Cu');

% Hanle measurement at 100 uA
field_range = linspace(-50e-3, 50e-3, 101);
results = device.measureHanle(100e-6, field_range);
device.plotResults('save_figures', true);
```

## Project Structure

```
spincirc/
├── matlab/          # MATLAB core (transport/LLG solvers, device models, tests)
├── python/          # Analysis tools (data processing, ML, visualization)
├── verilogA/        # SPICE compact models and test circuits
├── examples/        # Demo scripts
└── docs/            # Documentation
```

## Testing

```matlab
runtests('matlab/tests');
```

```bash
pytest python/tests/ -v --cov=python
```

## Citation

```bibtex
@article{alawein2018circuit,
  title={Circuit Models for Spintronic Devices Subject to Electric and Magnetic Fields},
  author={Alawein, Meshal and Fariborzi, Hamid},
  journal={IEEE Journal on Exploratory Solid-State Computational Devices and Circuits},
  volume={4},
  number={2},
  pages={76--85},
  year={2018},
  publisher={IEEE},
  doi={10.1109/JXCDC.2018.2848670}
}
```

## License

MIT License -- see [LICENSE](LICENSE).

## Author

**Meshal Alawein**
- Email: [contact@meshal.ai](mailto:contact@meshal.ai)
- GitHub: [github.com/alawein](https://github.com/alawein)
- LinkedIn: [linkedin.com/in/alawein](https://linkedin.com/in/alawein)
