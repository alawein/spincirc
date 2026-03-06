"""
Pytest configuration and shared fixtures for SpinCirc tests.

Provides synthetic IV curves, transport data, and common test
infrastructure for ML-based parameter extraction testing.

Author: Meshal Alawein
Email: meshal@berkeley.edu
License: MIT
"""

import sys
from unittest.mock import MagicMock

# Pre-mock optional dependencies so ml_tools.__init__ can import cleanly.
# We mock individual heavy packages (not installed in CI) and ml_tools
# submodules that depend on them. surrogate_models is NOT mocked here
# because its deps (xgboost, optuna) are individually mocked below.
# NOTE: Do NOT mock torch at module level — it breaks scipy's is_torch_array check.
for _mod in [
    "xgboost", "optuna",
    "pymoo", "pymoo.algorithms", "pymoo.algorithms.moo",
    "pymoo.algorithms.moo.nsga2", "pymoo.algorithms.moo.nsga3",
    "pymoo.core", "pymoo.core.problem", "pymoo.optimize",
    "pymoo.termination", "pymoo.visualization", "pymoo.visualization.scatter",
    "ml_tools.device_optimization", "ml_tools.physics_informed_nn",
    "ml_tools.uncertainty_quantification",
]:
    sys.modules.setdefault(_mod, MagicMock())

import pytest
import numpy as np
import logging

logging.basicConfig(level=logging.WARNING)


@pytest.fixture
def rng():
    """Deterministic random number generator for reproducible tests."""
    return np.random.RandomState(42)


@pytest.fixture
def synthetic_iv_linear():
    """Synthetic linear IV curve (Ohmic device, R=1 kOhm)."""
    voltage = np.linspace(-1.0, 1.0, 101)
    resistance = 1e3  # 1 kOhm
    current = voltage / resistance
    return voltage, current


@pytest.fixture
def synthetic_iv_diode():
    """Synthetic diode-like IV curve (exponential forward bias)."""
    voltage = np.linspace(-0.5, 1.0, 151)
    I_s = 1e-12  # Reverse saturation current (A)
    V_T = 0.026  # Thermal voltage at 300K (V)
    current = I_s * (np.exp(voltage / V_T) - 1)
    # Clip to avoid overflow in features
    current = np.clip(current, -1e-3, 1e-3)
    return voltage, current


@pytest.fixture
def synthetic_iv_mtj():
    """
    Synthetic MTJ IV curve with TMR effect.
    Two resistance states: parallel (low R) and antiparallel (high R).
    """
    voltage = np.linspace(-0.5, 0.5, 201)
    R_P = 500    # Parallel resistance (Ohm)
    R_AP = 1500  # Antiparallel resistance (Ohm)
    TMR = (R_AP - R_P) / R_P  # TMR ratio = 2.0

    # Parallel state IV (with slight nonlinearity)
    current_P = voltage / R_P * (1 + 0.1 * voltage**2)
    # Antiparallel state IV
    current_AP = voltage / R_AP * (1 + 0.15 * voltage**2)

    return {
        "voltage": voltage,
        "current_P": current_P,
        "current_AP": current_AP,
        "R_P": R_P,
        "R_AP": R_AP,
        "TMR": TMR,
    }


@pytest.fixture
def synthetic_transport_data(rng):
    """Synthetic spin transport measurement data."""
    n_samples = 100
    temperature = np.linspace(10, 300, n_samples)  # K
    # Spin diffusion length decreases with temperature
    lambda_sf = 500e-9 * np.exp(-temperature / 200)  # m
    # Conductivity with metallic behavior
    sigma = 1e7 * (1 - 0.003 * temperature)  # S/m
    # Spin polarization
    P = 0.4 * (1 - (temperature / 1000) ** 2)

    return {
        "temperature": temperature,
        "spin_diffusion_length": lambda_sf,
        "conductivity": sigma,
        "spin_polarization": P,
    }


@pytest.fixture
def training_features_and_params(rng):
    """
    Synthetic training data for supervised parameter extraction.
    50 samples, 13 features, 3 target parameters.
    """
    n_samples = 50
    n_features = 13
    n_params = 3

    features = rng.randn(n_samples, n_features)
    # Target parameters: [alpha, gamma, R_contact]
    parameters = np.column_stack([
        rng.uniform(0.001, 0.1, n_samples),     # alpha
        rng.uniform(1e10, 3e11, n_samples),      # gamma
        rng.uniform(100, 10000, n_samples),       # R_contact
    ])

    return features, parameters


@pytest.fixture
def parameter_bounds():
    """Standard parameter bounds for extraction."""
    return {
        "alpha": (0.001, 0.1),
        "gamma": (1e10, 3e11),
        "R_contact": (100, 10000),
    }


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow"
    )
    config.addinivalue_line(
        "markers", "integration: marks integration tests"
    )
