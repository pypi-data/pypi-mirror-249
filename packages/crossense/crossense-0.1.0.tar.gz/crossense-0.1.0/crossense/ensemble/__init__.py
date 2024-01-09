"""
The :mod:`crossense.ensemble` module includes ensemble-based methods for
classification, regression and anomaly detection.
"""
from ._bagging import BaseCrossBagging, CrossBaggingClassifier, CrossBaggingRegressor

__all__ = [
    "BaseCrossBagging",
    "CrossBaggingClassifier",
    "CrossBaggingRegressor",
]
