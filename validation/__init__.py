"""
Atlas AI Trading Platform 3.3

Validation Framework

Provides statistical validation tools for
quantitative strategy research.

Modules:

- WindowGenerator
- WalkForwardValidator
- ValidationMetrics
- ValidationReport
"""

from .window import WindowGenerator
from .walk_forward import WalkForwardValidator
from .metrics import ValidationMetrics
from .report import ValidationReport

__all__ = [
    "WindowGenerator",
    "WalkForwardValidator",
    "ValidationMetrics",
    "ValidationReport",
]