"""
Atlas AI Trading Platform 4.0

Adaptive Strategy Router

Routes detected market regimes
to specialised strategies.

Supports:

- Trend markets
- Range markets
- Volatility markets
- Unknown regimes
- Future AI regime confidence
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



        regime = str(regime).upper().strip()





        # =====================================================
        # TREND CONDITIONS
        # =====================================================

        if regime in (

            "TREND",

            "BULLISH",

            "BEARISH",

            "UPTREND",

            "DOWNTREND",

        ):


            return self.strategies["TREND"]





        # =====================================================
        # RANGE CONDITIONS
        # =====================================================

        if regime in (

            "RANGE",

            "SIDEWAYS",

            "CONSOLIDATION",

        ):


            return self.strategies["RANGE"]





        # =====================================================
        # VOLATILITY CONDITIONS
        # =====================================================

        if regime in (

            "VOLATILITY",

            "VOLATILE",

            "VOLATILE TREND",

            "BREAKOUT",

        ):


            return self.strategies["VOLATILITY"]





        # =====================================================
        # SAFE DEFAULT
        #
        # Unknown market states should not crash
        #
        # =====================================================

        return self.strategies["TREND"]
