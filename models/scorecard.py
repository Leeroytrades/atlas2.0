"""
Atlas AI Trading Platform

Scorecard Model

Represents the complete analysis for a symbol.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Scorecard:
    """
    Composite market analysis.
    """

    symbol: str = ""

    trend: int = 0

    momentum: int = 0

    volatility: int = 0

    volume: int = 0

    total_score: int = 0

    confidence: float = 0.0

    bullish: bool = False

    bearish: bool = False

    signal: str = "HOLD"

    timeframe: str = ""

    notes: str = ""

    @property
    def bias(self) -> str:

        if self.bullish:
            return "BUY"

        if self.bearish:
            return "SELL"

        return "NEUTRAL"

    @property
    def strength(self) -> str:

        score = self.total_score

        if score >= 90:
            return "EXTREME"

        if score >= 80:
            return "VERY STRONG"

        if score >= 70:
            return "STRONG"

        if score >= 60:
            return "MODERATE"

        if score >= 50:
            return "WEAK"

        return "AVOID"

    @property
    def tradable(self) -> bool:

        return self.total_score >= 70

    def summary(self) -> dict:

        return {

            "symbol": self.symbol,

            "score": self.total_score,

            "confidence": self.confidence,

            "bias": self.bias,

            "strength": self.strength,

            "signal": self.signal,

            "tradable": self.tradable,

        }

    def __str__(self):

        return (

            f"{self.symbol} | "

            f"{self.bias} | "

            f"{self.total_score}/100 | "

            f"{self.confidence:.1f}%"

        )