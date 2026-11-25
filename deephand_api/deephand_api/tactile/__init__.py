"""Tactile sensor backends and data types for the DeepHand hand."""

from .paxini import PaxiniConfig, PaxiniHandSensor
from .paxini_qt_visualizer import PaxiniQtVisualizer

__all__ = [
    "PaxiniConfig",
    "PaxiniHandSensor",
    "PaxiniQtVisualizer",
]
