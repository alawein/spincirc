"""
Tests for SpinCirc Surrogate Models Module.

Covers SurrogateConfig, SurrogateModelBuilder initialization,
training data handling, individual model builds (RF, GP, NN),
evaluation, prediction, feature importance, and save/load.

Since xgboost is not installed in CI, we mock it and skip XGBoost-specific tests.

Author: Meshal Alawein
Email: meshal@berkeley.edu
License: MIT
"""

import pytest
import numpy as np
import sys
import importlib
from pathlib import Path
from unittest.mock import MagicMock

# conftest.py already mocks heavy deps (xgboost, optuna, torch, pymoo, etc.)
# and keeps surrogate_models unmocked so we can import the real module.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ml_tools.surrogate_models import SurrogateConfig, SurrogateModelBuilder


# ── Fixtures ──────────────────────────────────────────────────────────


@pytest.fixture
def rng():
    return np.random.RandomState(42)


@pytest.fixture
def synthetic_regression_data(rng):
    """Simple regression dataset: y = 2*x1 + 3*x2 + noise."""
    n = 100
    X = rng.randn(n, 3)
    y = 2 * X[:, 0] + 3 * X[:, 1] + rng.randn(n) * 0.1
    return X, y.reshape(-1, 1)  # 2D targets required by SurrogateModelBuilder


@pytest.fixture
def builder_with_data(synthetic_regression_data):
    """SurrogateModelBuilder with training data loaded (no hyperopt)."""
    X, y = synthetic_regression_data
    config = SurrogateConfig(
        hyperparameter_tuning=False,
        test_size=0.2,
        random_state=42,
        verbose=False,
    )
    builder = SurrogateModelBuilder(config)
    builder.add_training_data(
        X, y,
        feature_names=["x1", "x2", "x3"],
        target_names=["y"],
    )
    return builder


# ── SurrogateConfig ───────────────────────────────────────────────────


class TestSurrogateConfig:
    """Tests for SurrogateConfig dataclass."""

    def test_default_values(self):
        config = SurrogateConfig()
        assert config.model_type == "gaussian_process"
        assert config.test_size == 0.2
        assert config.cv_folds == 5
        assert config.random_state == 42
        assert config.scale_features is True
        assert config.scale_targets is False
        assert config.hyperparameter_tuning is True
        assert config.verbose is True

    def test_custom_model_type(self):
        config = SurrogateConfig(model_type="rf")
        assert config.model_type == "rf"

    def test_ensemble_models_default(self):
        config = SurrogateConfig()
        assert "rf" in config.ensemble_models
        assert "xgb" in config.ensemble_models
        assert "gp" in config.ensemble_models


# ── SurrogateModelBuilder Init ────────────────────────────────────────


class TestSurrogateModelBuilderInit:
    """Tests for builder initialization."""

    def test_default_init(self):
        builder = SurrogateModelBuilder()
        assert builder.models == {}
        assert builder.best_model is None
        assert builder.feature_names == []

    def test_scalers_created(self):
        builder = SurrogateModelBuilder()
        assert builder.feature_scaler is not None

    def test_no_feature_scaler_when_disabled(self):
        config = SurrogateConfig(scale_features=False)
        builder = SurrogateModelBuilder(config)
        assert builder.feature_scaler is None


# ── add_training_data ─────────────────────────────────────────────────


class TestAddTrainingData:
    """Tests for training data handling."""

    def test_data_split(self, builder_with_data):
        assert builder_with_data.X_train is not None
        assert builder_with_data.X_test is not None
        assert builder_with_data.y_train is not None
        assert builder_with_data.y_test is not None

    def test_split_ratio(self, builder_with_data):
        total = len(builder_with_data.X_train) + len(builder_with_data.X_test)
        assert total == 100

    def test_feature_names_set(self, builder_with_data):
        assert builder_with_data.feature_names == ["x1", "x2", "x3"]

    def test_target_names_set(self, builder_with_data):
        assert builder_with_data.target_names == ["y"]

    def test_auto_feature_names(self, synthetic_regression_data):
        X, y = synthetic_regression_data
        builder = SurrogateModelBuilder(SurrogateConfig(hyperparameter_tuning=False))
        builder.add_training_data(X, y)
        assert builder.feature_names[0] == "feature_0"

    def test_1d_targets_reshaped(self, rng):
        X = rng.randn(20, 2)
        y = rng.randn(20)  # 1D
        builder = SurrogateModelBuilder(SurrogateConfig(hyperparameter_tuning=False))
        builder.add_training_data(X, y)
        assert builder.target_names == ["target"]


# ── build_random_forest ───────────────────────────────────────────────


class TestBuildRandomForest:
    """Tests for Random Forest model building."""

    def test_build_rf(self, builder_with_data):
        model = builder_with_data.build_random_forest()
        assert model is not None
        assert "rf" in builder_with_data.models

    def test_rf_can_predict(self, builder_with_data):
        builder_with_data.build_random_forest()
        preds = builder_with_data.models["rf"].predict(builder_with_data.X_test)
        assert len(preds) == len(builder_with_data.X_test)

    def test_rf_predictions_finite(self, builder_with_data):
        builder_with_data.build_random_forest()
        preds = builder_with_data.models["rf"].predict(builder_with_data.X_test)
        assert np.all(np.isfinite(preds))


# ── build_gaussian_process ────────────────────────────────────────────


class TestBuildGaussianProcess:
    """Tests for Gaussian Process model building."""

    def test_build_gp(self, builder_with_data):
        model = builder_with_data.build_gaussian_process()
        assert model is not None
        assert "gp" in builder_with_data.models

    def test_gp_can_predict(self, builder_with_data):
        builder_with_data.build_gaussian_process()
        preds = builder_with_data.models["gp"].predict(builder_with_data.X_test)
        assert len(preds) == len(builder_with_data.X_test)


# ── build_neural_network ──────────────────────────────────────────────


class TestBuildNeuralNetwork:
    """Tests for Neural Network model building."""

    def test_build_nn(self, builder_with_data):
        model = builder_with_data.build_neural_network()
        assert model is not None
        assert "nn" in builder_with_data.models

    def test_nn_predictions_finite(self, builder_with_data):
        builder_with_data.build_neural_network()
        preds = builder_with_data.models["nn"].predict(builder_with_data.X_test)
        assert np.all(np.isfinite(preds))


# ── evaluate_models ───────────────────────────────────────────────────


class TestEvaluateModels:
    """Tests for model evaluation."""

    def test_evaluate_single_model(self, builder_with_data):
        builder_with_data.build_random_forest()
        results = builder_with_data.evaluate_models()
        assert "rf" in results
        assert "r2" in results["rf"]
        assert "mse" in results["rf"]
        assert "mae" in results["rf"]

    def test_mse_nonnegative(self, builder_with_data):
        builder_with_data.build_random_forest()
        results = builder_with_data.evaluate_models()
        assert results["rf"]["mse"] >= 0

    def test_best_model_selected(self, builder_with_data):
        builder_with_data.build_random_forest()
        builder_with_data.evaluate_models()
        assert builder_with_data.best_model is not None


# ── predict ───────────────────────────────────────────────────────────


class TestPredict:
    """Tests for prediction interface."""

    def test_predict_with_best_model(self, builder_with_data):
        builder_with_data.build_random_forest()
        builder_with_data.evaluate_models()
        preds = builder_with_data.predict(builder_with_data.X_test)
        assert len(preds) == len(builder_with_data.X_test)

    def test_predict_with_named_model(self, builder_with_data):
        builder_with_data.build_random_forest()
        preds = builder_with_data.predict(
            builder_with_data.X_test, model_name="rf"
        )
        assert len(preds) > 0

    def test_predict_no_model_raises(self, builder_with_data):
        with pytest.raises((ValueError, KeyError)):
            builder_with_data.predict(builder_with_data.X_test)


# ── get_feature_importance ────────────────────────────────────────────


class TestGetFeatureImportance:
    """Tests for feature importance extraction."""

    def test_rf_has_importance(self, builder_with_data):
        builder_with_data.build_random_forest()
        importance = builder_with_data.get_feature_importance("rf")
        assert importance is not None
        assert "x1" in importance
        assert "x2" in importance

    def test_gp_no_importance(self, builder_with_data):
        builder_with_data.build_gaussian_process()
        importance = builder_with_data.get_feature_importance("gp")
        assert importance is None

    def test_nonexistent_model(self, builder_with_data):
        importance = builder_with_data.get_feature_importance("nonexistent")
        assert importance is None


# ── save/load model ───────────────────────────────────────────────────


class TestSaveLoadModel:
    """Tests for model persistence."""

    def test_save_and_load(self, builder_with_data, tmp_path):
        builder_with_data.build_random_forest()
        builder_with_data.evaluate_models()
        filepath = str(tmp_path / "model.joblib")

        builder_with_data.save_model(filepath, model_name="rf")

        new_builder = SurrogateModelBuilder()
        new_builder.load_model(filepath)
        assert new_builder.best_model is not None
        assert new_builder.feature_names == ["x1", "x2", "x3"]

    def test_save_no_model_raises(self):
        builder = SurrogateModelBuilder()
        with pytest.raises((ValueError, KeyError)):
            builder.save_model("/tmp/none.joblib")


if __name__ == "__main__":
    pytest.main([__file__])
