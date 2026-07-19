"""
Atlas AI Trading Assistant 2.0

Bull / Bear Scorecard Model
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Scorecard:
    """
    Stores individual indicator scores and calculates
    the overall Bull/Bear score.
    """

    # Trend
    trend: int = 0

    # Momentum
    momentum: int = 0

    # Volatility
    volatility: int = 0

    # Volume
    volume: int = 0

    # Overall confidence
    confidence: float = 0.0

    @property
    def total_score(self) -> int:
        """
        Total score.

        Maximum:
            +100

        Minimum:
            -100
        """

        score = (
            self.trend
            + self.momentum
            + self.volatility
            + self.volume
        )

        return max(-100, min(100, score))

    @property
    def bias(self) -> str:

        score = self.total_score

        if score >= 80:
            return "STRONG BUY"

        if score >= 60:
            return "BUY"

        if score >= 20:
            return "BULLISH"

        if score <= -80:
            return "STRONG SELL"

        if score <= -60:
            return "SELL"

        if score <= -20:
            return "BEARISH"

        return "NEUTRAL"

    @property
    def bullish(self) -> bool:
        return self.total_score > 20

    @property
    def bearish(self) -> bool:
        return self.total_score < -20

    def summary(self) -> dict:

        return {
            "Trend": self.trend,
            "Momentum": self.momentum,
            "Volatility": self.volatility,
            "Volume": self.volume,
            "Score": self.total_score,
            "Bias": self.bias,
            "Confidence": round(self.confidence * 100, 1),
        }