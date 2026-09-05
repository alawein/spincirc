"""Machine-learning helpers for SpinCirc data analysis.

Core extraction and surrogate utilities are available with scikit-learn.
Physics-informed neural-network tools require their optional deep-learning
runtime and are intentionally not imported at package import time.
"""

from .parameter_extraction import ParameterExtractor
from .surrogate_models import SurrogateModelBuilder

__all__ = ["ParameterExtractor", "SurrogateModelBuilder"]
