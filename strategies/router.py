"""
Atlas AI Trading Platform 3.6

Adaptive Strategy Router

Routes strategies using:

- Trend state
- Range detection
- Volatility state
- Momentum state

Designed for walk-forward validation.
"""

from __future__ import annotations


from strategy.trend_strategy import TrendStrategy
from strategy.range_strategy import RangeStrategy



class StrategyRouter:


    def __init__(self):


        self.strategies = {


            "TREND":

                TrendStrategy(),


            "RANGE":

                RangeStrategy(),


        }



    # =====================================================
    # REGIME NORMALISER
    # =====================================================

    def normalise(
        self,
        regime: str,
    ):


        if regime is None:

            return "TREND"



        regime = str(
            regime
        ).upper()



        # Trend environments

        if regime in (

            "BULLISH",

            "BEARISH",

            "TREND",

            "STRONG_TREND",

        ):

            return "TREND"



        # Range environments

        if regime in (

            "RANGE",

            "SIDEWAYS",

            "CONSOLIDATION",

            "MEAN_REVERSION",

        ):

            return "RANGE"



        # Volatility handling

        if "VOLATILE" in regime:


            return "TREND"



        return "TREND"



    # =====================================================
    # SELECT STRATEGY
    # =====================================================

    def select(
        self,
        regime: str,
    ):


        strategy_type = self.normalise(

            regime

        )


        return self.strategies.get(

            strategy_type,

            self.strategies["TREND"]

        )



    # =====================================================
    # AVAILABLE STRATEGIES
    # =====================================================

    def available(self):


        return list(

            self.strategies.keys()

        )