"""
Atlas AI Trading Platform 3.5

Strategy Selector

Adaptive strategy routing layer.

Uses market regime information
to select the appropriate strategy.

Flow:

Regime Detector

        |

Strategy Selector

        |

Trend Strategy
Range Strategy
Volatility Strategy
"""

from __future__ import annotations


from dataclasses import dataclass



@dataclass(slots=True)
class StrategySelection:

    name: str

    reason: str

    regime: str



class StrategySelector:


    """
    Determines which strategy
    should operate in the
    current market environment.
    """



    def __init__(self):

        self.available = {

            "TREND":
                "TrendStrategy",

            "RANGE":
                "RangeStrategy",

            "VOLATILE":
                "VolatilityStrategy",

        }



    # =====================================================
    # SELECT STRATEGY
    # =====================================================

    def select(
        self,
        regime_data: dict,
    ) -> StrategySelection:


        regime = regime_data.get(
            "regime",
            "UNKNOWN"
        )


        volatility = regime_data.get(
            "volatility",
            "NORMAL"
        )


        trend = regime_data.get(
            "trend",
            "SIDEWAYS"
        )



        # ---------------------------------
        # High volatility protection
        # ---------------------------------

        if volatility == "HIGH":

            return StrategySelection(

                name="VolatilityStrategy",

                reason=
                    "High volatility detected",

                regime=regime,

            )



        # ---------------------------------
        # Trending markets
        # ---------------------------------

        if (

            trend in (

                "BULLISH",
                "BEARISH"

            )

            and regime == "TREND"

        ):

            return StrategySelection(

                name="TrendStrategy",

                reason=
                    "Directional trend detected",

                regime=regime,

            )



        # ---------------------------------
        # Sideways markets
        # ---------------------------------

        if regime == "RANGE":

            return StrategySelection(

                name="RangeStrategy",

                reason=
                    "Mean reversion environment",

                regime=regime,

            )



        # ---------------------------------
        # Default
        # ---------------------------------

        return StrategySelection(

            name="TrendStrategy",

            reason=
                "Fallback strategy",

            regime=regime,

        )



    # =====================================================
    # SIMPLE NAME RETURN
    # =====================================================

    def strategy_name(
        self,
        regime_data: dict,
    ) -> str:


        return self.select(
            regime_data
        ).name