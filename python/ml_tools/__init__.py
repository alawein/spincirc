"""
SpinCirc Machine Learning Tools

Advanced ML tools for spintronic device modeling and optimization.

Author: Meshal Alawein <contact@meshal.ai>
Copyright © 2025 Meshal Alawein
License: MIT
"""

from .parameter_extraction import ParameterExtractor
from .device_optimization import DeviceOptimizer
from .physics_informed_nn import PhysicsInformedNN
from .surrogate_models import SurrogateModelBuilder
from .uncertainty_quantification import UncertaintyAnalyzer

__all__ = [
    'ParameterExtractor',
    'DeviceOptimizer', 
    'PhysicsInformedNN',
    'SurrogateModelBuilder',
    'UncertaintyAnalyzer'
]

__version__ = '1.0.0'