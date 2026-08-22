"""
Atlas AI Trading Platform 4.3

Adaptive Strategy Router

Routes validated market regimes to specialised strategies.

Supported regimes:

- TREND
- BULLISH
- BEARISH
- RANGE
- SIDEWAYS
- CONSOLIDATION
- VOLATILITY
- BREAKOUT
- UNKNOWN

UNKNOWN is deliberately NOT routed to a strategy.
"""

from __future__ import annotations

from strategy.trend_strategy import TrendStrategy
from strategy.range_strategy import RangeStrategy
from strategy.volatility_strategy import VolatilityStrategy


class StrategyRouter:

    def __init__(self):

        self.strategies = {

            "TREND":
                TrendStrategy(),

            "RANGE":
                RangeStrategy(),

            "VOLATILITY":
                VolatilityStrategy(),

        }

    # =====================================================
    # SELECT STRATEGY
    # =====================================================

    def select(
        self,
        regime: str,
    ):

        if regime is None:

            return None

        regime = str(
            regime
        ).upper().strip()

        # -------------------------------------------------
        # Trend
        # -------------------------------------------------

        if regime in (
            "TREND",
            "BULLISH",
            "BEARISH",
            "UPTREND",
            "DOWNTREND",
        ):

            return self.strategies[
                "TREND"
            ]

        # -------------------------------------------------
        # Range
        # -------------------------------------------------

        if regime in (
            "RANGE",
            "SIDEWAYS",
            "CONSOLIDATION",
        ):

            return self.strategies[
                "RANGE"
            ]

        # -------------------------------------------------
        # Volatility
        # -------------------------------------------------

        if regime in (
            "VOLATILITY",
            "VOLATILE",
            "VOLATILE TREND",
            "BREAKOUT",
        ):

            return self.strategies[
                "VOLATILITY"
            ]

        # -------------------------------------------------
        # UNKNOWN / UNSUPPORTED
        #
        # NEVER silently convert UNKNOWN into TREND.
        # -------------------------------------------------

        return None