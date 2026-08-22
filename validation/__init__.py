"""
Atlas AI Trading Platform 4.1

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
from .metrics import ValidationMetrics
from .report import ValidationReport

__all__ = [
    "WindowGenerator",
    "ValidationMetrics",
    "ValidationReport",
]