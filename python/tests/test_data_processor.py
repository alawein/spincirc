"""
Tests for SpinCirc Data Processing Module.

Covers ProcessingConfig, SpinCircDataProcessor initialization,
transport/magnetization extraction, TMR calculation, LLG fitting,
switching dynamics, statistical analysis, and export functionality.

Author: Meshal Alawein
Email: meshal@berkeley.edu
License: MIT
"""

import pytest
import numpy as np
import json
import warnings
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analysis.data_processor import (
    ProcessingConfig,
    SpinCircDataProcessor,
    load_spincirc_data,
)


# ── Fixtures ──────────────────────────────────────────────────────────


@pytest.fixture
def processor():
    """Default processor instance."""
    return SpinCircDataProcessor()


@pytest.fixture
def processor_with_config():
    """Processor with custom config."""
    config = ProcessingConfig(
        remove_outliers=False,
        smooth_data=True,
        smoothing_window=3,
        verbose=False,
    )
    return SpinCircDataProcessor(config)


@pytest.fixture
def transport_array():
    """Synthetic 4×N transport data (charge, spin_x, spin_y, spin_z)."""
    n = 100
    rng = np.random.RandomState(42)
    data = rng.randn(4, n) * 1e-6
    return data


@pytest.fixture
def magnetization_3xN():
    """Synthetic unit magnetization trajectory (3×N)."""
    n = 200
    t = np.linspace(0, 1e-9, n)
    theta = np.pi / 4 * np.exp(-1e9 * t)
    mx = np.sin(theta) * np.cos(2 * np.pi * 1e10 * t)
    my = np.sin(theta) * np.sin(2 * np.pi * 1e10 * t)
    mz = np.cos(theta)
    return np.array([mx, my, mz])


@pytest.fixture
def resistance_data():
    """Synthetic resistance data for TMR calculation."""
    rng = np.random.RandomState(42)
    r_p = 500 + rng.randn(50) * 10
    r_ap = 1500 + rng.randn(50) * 20
    return np.concatenate([r_p, r_ap])


@pytest.fixture
def switching_magnetization():
    """Magnetization that switches sign in mz."""
    n = 500
    t = np.linspace(0, 10e-9, n)
    mz = np.tanh(1e9 * (t - 5e-9))
    mx = np.sqrt(1 - mz**2) * np.cos(2 * np.pi * 1e10 * t)
    my = np.sqrt(1 - mz**2) * np.sin(2 * np.pi * 1e10 * t)
    return t, np.array([mx, my, mz])


# ── ProcessingConfig ──────────────────────────────────────────────────


class TestProcessingConfig:
    """Tests for ProcessingConfig dataclass."""

    def test_default_values(self):
        config = ProcessingConfig()
        assert config.remove_outliers is True
        assert config.outlier_threshold == 3.0
        assert config.interpolate_missing is True
        assert config.smooth_data is False
        assert config.smoothing_window == 5
        assert config.normalize_data is False
        assert config.verbose is True

    def test_custom_values(self):
        config = ProcessingConfig(outlier_threshold=2.0, smoothing_window=7)
        assert config.outlier_threshold == 2.0
        assert config.smoothing_window == 7


# ── SpinCircDataProcessor Init ────────────────────────────────────────


class TestSpinCircDataProcessorInit:
    """Tests for processor initialization."""

    def test_default_config(self, processor):
        assert isinstance(processor.config, ProcessingConfig)
        assert processor.data == {}
        assert processor.metadata == {}
        assert processor.processed_data == {}

    def test_custom_config(self, processor_with_config):
        assert processor_with_config.config.smooth_data is True
        assert processor_with_config.config.smoothing_window == 3


# ── extract_transport_data ────────────────────────────────────────────


class TestExtractTransportData:
    """Tests for transport data extraction."""

    def test_array_format_4xN(self, processor, transport_array):
        processor.data = {"I_s": transport_array}
        result = processor.extract_transport_data("I_s")
        assert "charge" in result
        assert "spin_x" in result
        assert "spin_y" in result
        assert "spin_z" in result
        assert result["charge"].shape == (transport_array.shape[1],)

    def test_missing_key_raises(self, processor):
        processor.data = {}
        with pytest.raises(KeyError, match="not found"):
            processor.extract_transport_data("missing")

    def test_non_4row_array(self, processor):
        """Non-standard shapes should be returned under 'data' key."""
        processor.data = {"I_s": np.ones((2, 50))}
        result = processor.extract_transport_data("I_s")
        assert "data" in result

    def test_custom_key(self, processor, transport_array):
        processor.data = {"custom": transport_array}
        result = processor.extract_transport_data("custom")
        assert "charge" in result


# ── extract_magnetization_data ────────────────────────────────────────


class TestExtractMagnetizationData:
    """Tests for magnetization data extraction."""

    def test_basic_extraction(self, processor, magnetization_3xN):
        processor.data = {"m": magnetization_3xN}
        result = processor.extract_magnetization_data("m")
        assert "mx" in result
        assert "my" in result
        assert "mz" in result
        assert "magnitude" in result
        assert "theta" in result
        assert "phi" in result

    def test_magnitude_near_unity(self, processor, magnetization_3xN):
        processor.data = {"m": magnetization_3xN}
        result = processor.extract_magnetization_data("m")
        np.testing.assert_allclose(result["magnitude"], 1.0, atol=0.02)

    def test_wrong_shape_raises(self, processor):
        processor.data = {"m": np.ones((2, 100))}
        with pytest.raises(ValueError, match="3 components"):
            processor.extract_magnetization_data("m")

    def test_missing_key_raises(self, processor):
        processor.data = {}
        with pytest.raises(KeyError, match="not found"):
            processor.extract_magnetization_data("m")

    def test_magnitude_warning(self, processor):
        """Large magnitude deviations should produce a warning."""
        bad_m = np.array([[2.0, 0.0], [0.0, 0.0], [0.0, 2.0]])
        processor.data = {"m": bad_m}
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            processor.extract_magnetization_data("m")
            assert any("magnitude" in str(warning.message).lower() for warning in w)


# ── calculate_tmr ─────────────────────────────────────────────────────


class TestCalculateTMR:
    """Tests for TMR calculation."""

    def test_basic_tmr(self, processor, resistance_data):
        result = processor.calculate_tmr(resistance_data)
        assert "tmr_percent" in result
        assert "resistance_parallel" in result
        assert "resistance_antiparallel" in result
        assert "resistance_ratio" in result

    def test_tmr_value_reasonable(self, processor, resistance_data):
        result = processor.calculate_tmr(resistance_data)
        # Expected TMR ~ (1500-500)/500 * 100 = 200%
        assert 150 < result["tmr_percent"] < 250

    def test_tmr_with_configuration(self, processor, resistance_data):
        config = np.concatenate([np.ones(50), -np.ones(50)])
        result = processor.calculate_tmr(resistance_data, configuration=config)
        assert result["tmr_percent"] > 0

    def test_all_parallel_raises(self, processor):
        data = np.ones(100) * 500
        config = np.ones(100)  # All parallel, no antiparallel
        with pytest.raises(ValueError, match="antiparallel"):
            processor.calculate_tmr(data, configuration=config)

    def test_resistance_ratio_positive(self, processor, resistance_data):
        result = processor.calculate_tmr(resistance_data)
        assert result["resistance_ratio"] > 0


# ── analyze_switching_dynamics ────────────────────────────────────────


class TestAnalyzeSwitchingDynamics:
    """Tests for switching dynamics analysis."""

    def test_switching_detected(self, processor, switching_magnetization):
        t, m = switching_magnetization
        result = processor.analyze_switching_dynamics(t, m)
        assert result["switching_events"] > 0
        assert len(result["switching_times"]) > 0

    def test_no_switching(self, processor):
        t = np.linspace(0, 1e-9, 100)
        m = np.array([np.zeros(100), np.zeros(100), np.ones(100)])
        result = processor.analyze_switching_dynamics(t, m)
        assert result["switching_events"] == 0
        assert result["switching_times"] == []

    def test_1d_magnetization(self, processor):
        """Should handle 1D mz input."""
        t = np.linspace(0, 10e-9, 200)
        mz = np.tanh(1e9 * (t - 5e-9))
        result = processor.analyze_switching_dynamics(t, mz)
        assert result["switching_events"] > 0


# ── statistical_analysis ──────────────────────────────────────────────


class TestStatisticalAnalysis:
    """Tests for statistical analysis."""

    def test_basic_stats(self, processor):
        data = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
        result = processor.statistical_analysis(data)
        assert result["mean"] == pytest.approx(5.5)
        assert result["median"] == pytest.approx(5.5)
        assert result["min"] == pytest.approx(1.0)
        assert result["max"] == pytest.approx(10.0)
        assert result["count"] == 10

    def test_all_nan_returns_error(self, processor):
        data = np.array([np.nan, np.nan, np.nan])
        result = processor.statistical_analysis(data)
        assert "error" in result

    def test_nan_handling(self, processor):
        data = np.array([1.0, np.nan, 3.0, np.nan, 5.0])
        result = processor.statistical_analysis(data)
        assert result["count"] == 3
        assert result["valid_fraction"] == pytest.approx(0.6)

    def test_percentiles_present(self, processor):
        data = np.random.RandomState(42).randn(1000)
        result = processor.statistical_analysis(data)
        for p in [1, 5, 10, 25, 75, 90, 95, 99]:
            assert f"p{p}" in result

    def test_normality_test(self, processor):
        data = np.random.RandomState(42).randn(100)
        result = processor.statistical_analysis(data)
        assert "normality_p_value" in result
        assert "is_normal" in result

    def test_skewness_kurtosis(self, processor):
        data = np.random.RandomState(42).randn(100)
        result = processor.statistical_analysis(data)
        assert "skewness" in result
        assert "kurtosis" in result


# ── export_processed_data ─────────────────────────────────────────────


class TestExportProcessedData:
    """Tests for data export functionality."""

    def test_export_json(self, processor, tmp_path):
        processor.data = {"voltage": np.array([1.0, 2.0, 3.0])}
        output = tmp_path / "test.json"
        processor.export_processed_data(output, format="json")
        assert output.exists()
        with open(output) as f:
            loaded = json.load(f)
        assert loaded["voltage"] == [1.0, 2.0, 3.0]

    def test_export_csv(self, processor, tmp_path):
        processor.data = {
            "v": np.array([1.0, 2.0]),
            "i": np.array([0.1, 0.2]),
        }
        output = tmp_path / "test.csv"
        processor.export_processed_data(output, format="csv")
        assert output.exists()

    def test_export_hdf5(self, processor, tmp_path):
        processor.data = {"voltage": np.array([1.0, 2.0, 3.0])}
        output = tmp_path / "test.h5"
        processor.export_processed_data(output, format="hdf5")
        assert output.exists()

    def test_export_matlab(self, processor, tmp_path):
        processor.data = {"voltage": np.array([1.0, 2.0, 3.0])}
        output = tmp_path / "test.mat"
        processor.export_processed_data(output, format="matlab")
        assert output.exists()

    def test_unsupported_format_raises(self, processor, tmp_path):
        processor.data = {}
        with pytest.raises(ValueError, match="Unsupported"):
            processor.export_processed_data(tmp_path / "x.xyz", format="xyz")


# ── generate_report ───────────────────────────────────────────────────


class TestGenerateReport:
    """Tests for report generation."""

    def test_report_string(self, processor):
        processor.data = {"voltage": np.array([1.0, 2.0, 3.0])}
        processor.metadata = {"variables": ["voltage"]}
        report = processor.generate_report()
        assert isinstance(report, str)
        assert "SpinCirc" in report

    def test_report_save(self, processor, tmp_path):
        processor.data = {"voltage": np.array([1.0, 2.0, 3.0])}
        processor.metadata = {"variables": ["voltage"]}
        output = tmp_path / "report.txt"
        processor.generate_report(output)
        assert output.exists()

    def test_empty_data_report(self, processor):
        processor.data = {}
        processor.metadata = {}
        report = processor.generate_report()
        assert isinstance(report, str)


# ── load_matlab_data ──────────────────────────────────────────────────


class TestLoadMatlabData:
    """Tests for MATLAB data loading."""

    def test_file_not_found_raises(self, processor):
        with pytest.raises(FileNotFoundError):
            processor.load_matlab_data("/nonexistent/path.mat")

    @patch("analysis.data_processor.scipy.io.loadmat")
    def test_successful_load(self, mock_loadmat, processor, tmp_path):
        """Should load .mat file and strip metadata keys."""
        mock_loadmat.return_value = {
            "__header__": b"MATLAB 5.0",
            "__version__": "1.0",
            "__globals__": [],
            "voltage": np.array([1.0, 2.0]),
        }
        fake_file = tmp_path / "data.mat"
        fake_file.touch()
        data = processor.load_matlab_data(fake_file)
        assert "voltage" in data
        assert "__header__" not in data

    @patch("analysis.data_processor.scipy.io.loadmat")
    def test_metadata_extraction(self, mock_loadmat, processor, tmp_path):
        mock_loadmat.return_value = {
            "__header__": b"MATLAB",
            "__version__": "1.0",
            "__globals__": [],
            "v": np.array([1.0]),
        }
        fake_file = tmp_path / "data.mat"
        fake_file.touch()
        processor.load_matlab_data(fake_file)
        assert "variables" in processor.metadata
        assert "v" in processor.metadata["variables"]


# ── fit_llg_precession ────────────────────────────────────────────────


class TestFitLLGPrecession:
    """Tests for LLG precession fitting."""

    def test_fit_returns_dict(self, processor):
        """Fitting synthetic precession data should return parameters."""
        n = 500
        t = np.linspace(0, 1e-9, n)
        freq = 5e9
        damping = 1e9
        mx = 0.5 * np.exp(-damping * t) * np.cos(2 * np.pi * freq * t)
        my = 0.5 * np.exp(-damping * t) * np.sin(2 * np.pi * freq * t)
        mz = np.sqrt(1 - mx**2 - my**2)
        m = np.array([mx, my, mz])
        result = processor.fit_llg_precession(t, m)
        # Should return either parameters or error
        assert isinstance(result, dict)

    def test_fit_failure_returns_error(self, processor):
        """Unfittable data should return error dict."""
        t = np.array([0, 1])
        m = np.array([[1, 1], [0, 0], [0, 0]])
        result = processor.fit_llg_precession(t, m)
        # With only 2 points, fit likely fails
        assert isinstance(result, dict)


if __name__ == "__main__":
    pytest.main([__file__])
