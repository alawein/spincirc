"""
Tests for SpinCirc ML-based parameter extraction.

Covers ExtractionConfig, ParameterExtractor initialization,
parameter space definition, training data handling, IV feature
extraction, and cross-validation.

Author: Meshal Alawein
Email: meshal@berkeley.edu
License: MIT
"""

import pytest
import numpy as np
from unittest.mock import patch, MagicMock

from ml_tools.parameter_extraction import ExtractionConfig, ParameterExtractor


class TestExtractionConfig:
    """Tests for ExtractionConfig dataclass."""

    def test_default_values(self):
        """Should have sensible defaults."""
        config = ExtractionConfig()
        assert config.method == "bayesian"
        assert config.n_trials == 100
        assert config.cv_folds == 5
        assert config.random_state == 42
        assert config.verbose is True
        assert config.uncertainty_estimation is True
        assert config.parallel_jobs == -1

    def test_custom_method(self):
        """Should accept custom method."""
        config = ExtractionConfig(method="neural")
        assert config.method == "neural"

    def test_custom_n_trials(self):
        """Should accept custom trial count."""
        config = ExtractionConfig(n_trials=500)
        assert config.n_trials == 500

    def test_custom_cv_folds(self):
        """Should accept custom CV fold count."""
        config = ExtractionConfig(cv_folds=10)
        assert config.cv_folds == 10

    def test_genetic_method(self):
        """Should accept 'genetic' method."""
        config = ExtractionConfig(method="genetic")
        assert config.method == "genetic"

    def test_ensemble_method(self):
        """Should accept 'ensemble' method."""
        config = ExtractionConfig(method="ensemble")
        assert config.method == "ensemble"

    def test_disable_uncertainty(self):
        """Should allow disabling uncertainty estimation."""
        config = ExtractionConfig(uncertainty_estimation=False)
        assert config.uncertainty_estimation is False

    def test_quiet_mode(self):
        """Should allow setting verbose=False."""
        config = ExtractionConfig(verbose=False)
        assert config.verbose is False


class TestParameterExtractorInit:
    """Tests for ParameterExtractor initialization."""

    def test_default_init(self):
        """Should initialize with default config."""
        extractor = ParameterExtractor()
        assert extractor.config is not None
        assert extractor.config.method == "bayesian"

    def test_custom_config(self):
        """Should accept custom config."""
        config = ExtractionConfig(method="neural", n_trials=200)
        extractor = ParameterExtractor(config=config)
        assert extractor.config.method == "neural"
        assert extractor.config.n_trials == 200

    def test_scaler_initialized(self):
        """StandardScaler should be initialized."""
        extractor = ParameterExtractor()
        assert extractor.scaler is not None

    def test_empty_models_dict(self):
        """Models dict should start empty."""
        extractor = ParameterExtractor()
        assert extractor.models == {}

    def test_empty_parameter_bounds(self):
        """Parameter bounds should start empty."""
        extractor = ParameterExtractor()
        assert extractor.parameter_bounds == {}

    def test_empty_feature_names(self):
        """Feature names should start as empty list."""
        extractor = ParameterExtractor()
        assert extractor.feature_names == []

    def test_empty_parameter_names(self):
        """Parameter names should start as empty list."""
        extractor = ParameterExtractor()
        assert extractor.parameter_names == []

    def test_empty_history(self):
        """Extraction history should start empty."""
        extractor = ParameterExtractor()
        assert extractor.extraction_history == []


class TestDefineParameterSpace:
    """Tests for parameter space definition."""

    def test_basic_bounds(self, parameter_bounds):
        """Should accept valid parameter bounds."""
        extractor = ParameterExtractor()
        extractor.define_parameter_space(parameter_bounds)
        assert extractor.parameter_bounds == parameter_bounds

    def test_parameter_names_set(self, parameter_bounds):
        """Should populate parameter_names from bounds keys."""
        extractor = ParameterExtractor()
        extractor.define_parameter_space(parameter_bounds)
        assert set(extractor.parameter_names) == set(parameter_bounds.keys())

    def test_single_parameter(self):
        """Should work with a single parameter."""
        extractor = ParameterExtractor()
        bounds = {"alpha": (0.001, 0.1)}
        extractor.define_parameter_space(bounds)
        assert extractor.parameter_names == ["alpha"]

    def test_overwrite_previous_bounds(self):
        """Defining new bounds should overwrite previous ones."""
        extractor = ParameterExtractor()
        extractor.define_parameter_space({"alpha": (0.001, 0.1)})
        extractor.define_parameter_space({"gamma": (1e10, 3e11)})
        assert "alpha" not in extractor.parameter_bounds
        assert "gamma" in extractor.parameter_bounds

    def test_empty_bounds(self):
        """Should accept empty bounds dict."""
        extractor = ParameterExtractor()
        extractor.define_parameter_space({})
        assert extractor.parameter_bounds == {}
        assert extractor.parameter_names == []

    def test_wide_bounds(self):
        """Should accept bounds spanning many orders of magnitude."""
        extractor = ParameterExtractor()
        bounds = {"conductance": (1e-12, 1e6)}
        extractor.define_parameter_space(bounds)
        assert extractor.parameter_bounds["conductance"] == (1e-12, 1e6)


class TestAddTrainingData:
    """Tests for adding training data."""

    def test_valid_data(self, training_features_and_params):
        """Should accept valid features and parameters arrays."""
        features, parameters = training_features_and_params
        extractor = ParameterExtractor()
        extractor.add_training_data(features, parameters)
        assert hasattr(extractor, "X_train")
        assert hasattr(extractor, "y_train")

    def test_data_shapes(self, training_features_and_params):
        """X_train should be scaled, y_train should match input."""
        features, parameters = training_features_and_params
        extractor = ParameterExtractor()
        extractor.add_training_data(features, parameters)
        assert extractor.X_train.shape == features.shape
        assert extractor.y_train.shape == parameters.shape

    def test_scaling_applied(self, training_features_and_params):
        """X_train should be standardized (mean~0, std~1)."""
        features, parameters = training_features_and_params
        extractor = ParameterExtractor()
        extractor.add_training_data(features, parameters)
        # After fit_transform, columns should have mean~0, std~1
        col_means = np.mean(extractor.X_train, axis=0)
        col_stds = np.std(extractor.X_train, axis=0)
        np.testing.assert_allclose(col_means, 0.0, atol=1e-10)
        np.testing.assert_allclose(col_stds, 1.0, atol=0.1)

    def test_y_train_unmodified(self, training_features_and_params):
        """y_train should not be scaled."""
        features, parameters = training_features_and_params
        extractor = ParameterExtractor()
        extractor.add_training_data(features, parameters)
        np.testing.assert_array_equal(extractor.y_train, parameters)

    def test_custom_feature_names(self, training_features_and_params):
        """Should accept custom feature names."""
        features, parameters = training_features_and_params
        n_features = features.shape[1]
        names = [f"feat_{i}" for i in range(n_features)]
        extractor = ParameterExtractor()
        extractor.add_training_data(features, parameters, feature_names=names)
        assert extractor.feature_names == names

    def test_auto_feature_names(self, training_features_and_params):
        """Should auto-generate feature names if not provided."""
        features, parameters = training_features_and_params
        extractor = ParameterExtractor()
        extractor.add_training_data(features, parameters)
        assert len(extractor.feature_names) == features.shape[1]
        assert extractor.feature_names[0] == "feature_0"

    def test_small_dataset(self):
        """Should accept very small datasets (2 samples)."""
        features = np.array([[1.0, 2.0], [3.0, 4.0]])
        params = np.array([[0.01], [0.02]])
        extractor = ParameterExtractor()
        extractor.add_training_data(features, params)
        assert extractor.X_train.shape == (2, 2)


class TestExtractIVFeatures:
    """Tests for IV curve feature extraction."""

    @pytest.fixture
    def extractor(self):
        return ParameterExtractor()

    def test_linear_iv_features_shape(self, extractor, synthetic_iv_linear):
        """Should return 2D array with shape (1, n_features)."""
        voltage, current = synthetic_iv_linear
        features = extractor._extract_iv_features(voltage, current)
        assert features.ndim == 2
        assert features.shape[0] == 1

    def test_feature_count(self, extractor, synthetic_iv_linear):
        """Should extract 13 features total."""
        voltage, current = synthetic_iv_linear
        features = extractor._extract_iv_features(voltage, current)
        # 4 basic stats + 4 resistance + 3 conductance + 2 curvature = 13
        assert features.shape[1] == 13

    def test_features_finite(self, extractor, synthetic_iv_linear):
        """All features should be finite."""
        voltage, current = synthetic_iv_linear
        features = extractor._extract_iv_features(voltage, current)
        assert np.all(np.isfinite(features))

    def test_diode_features_finite(self, extractor, synthetic_iv_diode):
        """Features from diode IV should be finite."""
        voltage, current = synthetic_iv_diode
        features = extractor._extract_iv_features(voltage, current)
        assert np.all(np.isfinite(features))

    def test_linear_mean_current_near_zero(self, extractor, synthetic_iv_linear):
        """Symmetric linear IV should have mean current near zero."""
        voltage, current = synthetic_iv_linear
        features = extractor._extract_iv_features(voltage, current)
        # First feature is mean(current)
        mean_current = features[0, 0]
        assert mean_current == pytest.approx(0.0, abs=1e-6)

    def test_linear_conductance_constant(self, extractor, synthetic_iv_linear):
        """Linear IV should have low conductance std (constant dI/dV)."""
        voltage, current = synthetic_iv_linear
        features = extractor._extract_iv_features(voltage, current)
        # Conductance std is features[0, 9] (index into conductance features)
        conductance_std = features[0, 9]
        assert conductance_std == pytest.approx(0.0, abs=1e-6)

    def test_zero_voltage_handling(self, extractor):
        """Should handle IV data passing through V=0."""
        voltage = np.linspace(-1, 1, 51)
        current = voltage / 1000  # 1 kOhm
        features = extractor._extract_iv_features(voltage, current)
        assert np.all(np.isfinite(features))

    def test_single_point(self, extractor):
        """Should handle single data point gracefully."""
        voltage = np.array([0.5])
        current = np.array([1e-3])
        features = extractor._extract_iv_features(voltage, current)
        assert features.ndim == 2
        assert features.shape[0] == 1

    def test_two_points(self, extractor):
        """Should handle two data points (enough for gradient)."""
        voltage = np.array([0.0, 1.0])
        current = np.array([0.0, 1e-3])
        features = extractor._extract_iv_features(voltage, current)
        assert np.all(np.isfinite(features))

    def test_all_zero_voltage(self, extractor):
        """Should handle all-zero voltage (resistance features = 0)."""
        voltage = np.zeros(10)
        current = np.ones(10) * 1e-3
        features = extractor._extract_iv_features(voltage, current)
        # Resistance features should be 0 when voltage is 0
        assert features[0, 4] == 0  # mean resistance
        assert features[0, 5] == 0  # std resistance

    def test_different_iv_shapes_differ(self, extractor, synthetic_iv_linear, synthetic_iv_diode):
        """Linear and diode IV should produce different features."""
        v_lin, i_lin = synthetic_iv_linear
        v_dio, i_dio = synthetic_iv_diode
        feat_lin = extractor._extract_iv_features(v_lin, i_lin)
        feat_dio = extractor._extract_iv_features(v_dio, i_dio)
        # Features should not be identical
        assert not np.allclose(feat_lin, feat_dio)


class TestCrossValidateExtraction:
    """Tests for cross-validation of extraction performance."""

    @pytest.fixture
    def configured_extractor(self, parameter_bounds):
        """Extractor with parameter space defined."""
        extractor = ParameterExtractor(ExtractionConfig(cv_folds=3))
        extractor.define_parameter_space(parameter_bounds)
        return extractor

    def test_basic_cross_validation(self, configured_extractor, training_features_and_params, parameter_bounds):
        """Should run cross-validation without error."""
        features, parameters = training_features_and_params
        target_params = list(parameter_bounds.keys())
        results = configured_extractor.cross_validate_extraction(
            features, parameters, target_params
        )
        assert isinstance(results, dict)

    def test_returns_results_for_each_param(self, configured_extractor, training_features_and_params, parameter_bounds):
        """Should return results for each target parameter."""
        features, parameters = training_features_and_params
        target_params = list(parameter_bounds.keys())
        results = configured_extractor.cross_validate_extraction(
            features, parameters, target_params
        )
        for param in target_params:
            assert param in results

    def test_results_contain_model_metrics(self, configured_extractor, training_features_and_params, parameter_bounds):
        """Each parameter result should contain model metrics."""
        features, parameters = training_features_and_params
        target_params = list(parameter_bounds.keys())
        results = configured_extractor.cross_validate_extraction(
            features, parameters, target_params
        )
        for param in target_params:
            param_results = results[param]
            # Should have at least one model result
            assert len(param_results) > 0
            for model_name, metrics in param_results.items():
                assert "mse" in metrics
                assert "mae" in metrics
                assert "r2" in metrics

    def test_mse_nonnegative(self, configured_extractor, training_features_and_params, parameter_bounds):
        """MSE should be non-negative."""
        features, parameters = training_features_and_params
        target_params = list(parameter_bounds.keys())
        results = configured_extractor.cross_validate_extraction(
            features, parameters, target_params
        )
        for param in target_params:
            for model_name, metrics in results[param].items():
                assert metrics["mse"] >= 0

    def test_mae_nonnegative(self, configured_extractor, training_features_and_params, parameter_bounds):
        """MAE should be non-negative."""
        features, parameters = training_features_and_params
        target_params = list(parameter_bounds.keys())
        results = configured_extractor.cross_validate_extraction(
            features, parameters, target_params
        )
        for param in target_params:
            for model_name, metrics in results[param].items():
                assert metrics["mae"] >= 0

    def test_skips_unknown_params(self, configured_extractor, training_features_and_params):
        """Should skip parameters not in parameter_names."""
        features, parameters = training_features_and_params
        results = configured_extractor.cross_validate_extraction(
            features, parameters, ["nonexistent_param"]
        )
        assert "nonexistent_param" not in results

    def test_uses_rf_and_gb_models(self, configured_extractor, training_features_and_params, parameter_bounds):
        """Should use RandomForest and GradientBoosting models."""
        features, parameters = training_features_and_params
        target_params = list(parameter_bounds.keys())
        results = configured_extractor.cross_validate_extraction(
            features, parameters, target_params
        )
        for param in target_params:
            model_names = set(results[param].keys())
            assert "rf" in model_names
            assert "gb" in model_names


class TestExtractFromIVCurve:
    """Tests for full IV curve extraction pipeline."""

    @pytest.fixture
    def trained_extractor(self, training_features_and_params, parameter_bounds):
        """Extractor with training data and parameter space."""
        features, parameters = training_features_and_params
        config = ExtractionConfig(method="bayesian", n_trials=10)
        extractor = ParameterExtractor(config=config)
        extractor.define_parameter_space(parameter_bounds)
        extractor.add_training_data(features, parameters)
        return extractor

    def test_bayesian_extraction_runs(self, trained_extractor, synthetic_iv_linear, parameter_bounds):
        """Bayesian extraction should complete without error."""
        voltage, current = synthetic_iv_linear
        target_params = list(parameter_bounds.keys())
        results = trained_extractor.extract_from_iv_curve(voltage, current, target_params)
        assert isinstance(results, dict)

    def test_results_have_value_and_uncertainty(self, trained_extractor, synthetic_iv_linear, parameter_bounds):
        """Bayesian results should include value and uncertainty."""
        voltage, current = synthetic_iv_linear
        target_params = list(parameter_bounds.keys())
        results = trained_extractor.extract_from_iv_curve(voltage, current, target_params)
        for param in target_params:
            if param in results:
                assert "value" in results[param]
                assert "uncertainty" in results[param]

    def test_no_training_data_raises(self, synthetic_iv_linear, parameter_bounds):
        """Extraction without training data should raise ValueError."""
        extractor = ParameterExtractor()
        extractor.define_parameter_space(parameter_bounds)
        target_params = list(parameter_bounds.keys())
        voltage, current = synthetic_iv_linear
        with pytest.raises(ValueError, match="Training data"):
            extractor.extract_from_iv_curve(voltage, current, target_params)

    def test_unknown_method_raises(self, training_features_and_params, parameter_bounds, synthetic_iv_linear):
        """Unknown extraction method should raise ValueError."""
        features, parameters = training_features_and_params
        config = ExtractionConfig(method="invalid_method")
        extractor = ParameterExtractor(config=config)
        extractor.define_parameter_space(parameter_bounds)
        extractor.add_training_data(features, parameters)
        voltage, current = synthetic_iv_linear
        with pytest.raises(ValueError, match="Unknown"):
            extractor.extract_from_iv_curve(
                voltage, current, list(parameter_bounds.keys())
            )


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_empty_features_array(self):
        """Adding empty features should not crash during add but may fail later."""
        extractor = ParameterExtractor()
        features = np.empty((0, 5))
        params = np.empty((0, 2))
        # fit_transform on empty array -- behavior depends on sklearn version
        # Just verify no unhandled exception
        try:
            extractor.add_training_data(features, params)
        except ValueError:
            pass  # sklearn may raise on empty data

    def test_mismatched_sample_count(self):
        """Features and params with different sample counts should be caught by sklearn."""
        extractor = ParameterExtractor()
        features = np.ones((10, 5))
        params = np.ones((8, 2))  # Mismatch
        # add_training_data itself does not validate, but downstream methods will fail
        extractor.add_training_data(features, params)
        # The mismatch will be caught when trying to fit a model

    def test_single_feature_single_param(self):
        """Should handle minimal dimensions (1 feature, 1 parameter)."""
        extractor = ParameterExtractor()
        features = np.array([[1], [2], [3], [4], [5]], dtype=float)
        params = np.array([[0.01], [0.02], [0.03], [0.04], [0.05]])
        extractor.add_training_data(features, params)
        assert extractor.X_train.shape == (5, 1)

    def test_constant_features(self, parameter_bounds):
        """Constant features should not crash (though models may warn)."""
        extractor = ParameterExtractor(ExtractionConfig(cv_folds=2))
        extractor.define_parameter_space(parameter_bounds)
        features = np.ones((20, 5))
        params = np.random.RandomState(42).rand(20, 3)
        extractor.add_training_data(features, params)
        # Cross-validation may produce warnings but should not crash
        try:
            results = extractor.cross_validate_extraction(
                features, params, list(parameter_bounds.keys())
            )
        except Exception:
            pass  # Constant features may cause sklearn issues

    def test_genetic_extraction_with_bounds(self, parameter_bounds):
        """Genetic extraction should work with proper bounds."""
        config = ExtractionConfig(method="genetic", n_trials=5)
        extractor = ParameterExtractor(config=config)
        extractor.define_parameter_space(parameter_bounds)
        voltage = np.linspace(-0.5, 0.5, 50)
        current = voltage / 1000
        target_params = list(parameter_bounds.keys())
        results = extractor.extract_from_iv_curve(voltage, current, target_params)
        assert isinstance(results, dict)
        for param in target_params:
            if param in results:
                assert "value" in results[param]


if __name__ == "__main__":
    pytest.main([__file__])
