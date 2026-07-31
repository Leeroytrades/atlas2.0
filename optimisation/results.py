"""
Atlas AI Trading Platform 3.0

Optimisation Result Models
"""

from __future__ import annotations

from dataclasses import dataclass



@dataclass
class OptimisationResult:

    score_threshold: int

    confidence_threshold: float

    atr_stop: float

    atr_target: float

    net_profit: float

    win_rate: float

    profit_factor: float

    trades: int