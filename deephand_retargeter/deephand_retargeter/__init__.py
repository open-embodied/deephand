"""DeepHand hand retargeting wrappers.

This package intentionally depends on :mod:`dex_retargeting` instead of
copying its optimizer implementation. The DeepHand-specific layer owns robot
joint names, human landmark/vector mapping, passive-joint handling policy, and
output adapters for simulation or hardware callers.
"""

from .config import DeepHandRetargeterConfig
from .retargeter import DeepHandRetargeter, RetargetingResult
from .tuning import DEFAULT_TUNING, RetargeterTuning

__all__ = [
    "DEFAULT_TUNING",
    "DeepHandRetargeter",
    "DeepHandRetargeterConfig",
    "RetargetingResult",
    "RetargeterTuning",
]
