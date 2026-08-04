"""
Atlas AI Trading Platform 3.5

Adaptive Strategy Router

Routes detected market regimes
to specialised strategies.
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
    # SELECT STRATEGY
    # =====================================================

    def select(

        self,

        regime: str,

    ):


        regime = str(regime).upper()



        # -----------------------------
        # Trending markets
        # -----------------------------

        if regime in (

            "TREND",

            "BULLISH",

            "BEARISH",

        ):


            return self.strategies["TREND"]



        # -----------------------------
        # Range markets
        # -----------------------------

        if regime in (

            "RANGE",

            "SIDEWAYS",

        ):


            return self.strategies["RANGE"]



        # -----------------------------
        # Safe fallback
        # -----------------------------

        return self.strategies["TREND"]