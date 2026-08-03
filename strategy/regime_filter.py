"""
Atlas Regime Filter

Detects market conditions before strategy selection.
"""

from __future__ import annotations

import pandas as pd

from indicators.composite import build_indicator_set


class RegimeFilter:


    def __init__(
        self,
        allow_ranges: bool = False,
        allow_high_volatility: bool = True,
    ):

        self.allow_ranges = allow_ranges

        self.allow_high_volatility = allow_high_volatility


        self.total_checks = 0

        self.allowed_count = 0

        self.blocked_count = 0


        self.regime_counts = {

            "BULLISH": 0,

            "BEARISH": 0,

            "TREND": 0,

            "RANGE": 0,

            "UNKNOWN": 0,

        }



    # =====================================================
    # Evaluate Market Regime
    # =====================================================

    def evaluate(
        self,
        dataframe: pd.DataFrame,
    ) -> dict:


        self.total_checks += 1


        if dataframe is None or len(dataframe) < 50:

            self.blocked_count += 1

            self.regime_counts["UNKNOWN"] += 1

            return {

                "allowed": False,

                "reason": "INSUFFICIENT_DATA",

                "regime": "UNKNOWN",

            }



        # -------------------------------------------------
        # Ensure indicators exist
        # -------------------------------------------------

        required = [

            "EMA_20",

            "EMA_50",

            "ATR",

        ]


        missing = [

            col for col in required

            if col not in dataframe.columns

        ]


        if missing:

            dataframe = build_indicator_set(

                dataframe.copy()

            )



        latest = dataframe.iloc[-1]


        close = float(

            latest.get(

                "Close",

                0

            )

        )


        ema20 = float(

            latest.get(

                "EMA_20",

                close

            )

        )


        ema50 = float(

            latest.get(

                "EMA_50",

                close

            )

        )


        atr = float(

            latest.get(

                "ATR",

                0

            )

        )



        # -------------------------------------------------
        # Trend Detection
        # -------------------------------------------------

        if (

            close > ema20

            and ema20 > ema50

        ):

            regime = "BULLISH"



        elif (

            close < ema20

            and ema20 < ema50

        ):

            regime = "BEARISH"



        else:

            regime = "RANGE"



        self.regime_counts[regime] += 1



        # -------------------------------------------------
        # Volatility
        # -------------------------------------------------

        average_atr = dataframe["ATR"].mean()


        if average_atr == 0:

            volatility = "UNKNOWN"


        elif atr > average_atr * 1.25:

            volatility = "HIGH"


        elif atr < average_atr * 0.75:

            volatility = "LOW"


        else:

            volatility = "NORMAL"



        # -------------------------------------------------
        # Decision
        # -------------------------------------------------

        allowed = True

        reason = "REGIME_ACCEPTED"



        if regime == "RANGE":

            allowed = self.allow_ranges

            reason = "RANGE_BLOCKED"



        if (

            volatility == "HIGH"

            and not self.allow_high_volatility

        ):

            allowed = False

            reason = "HIGH_VOLATILITY_BLOCKED"



        if allowed:

            self.allowed_count += 1

        else:

            self.blocked_count += 1



        return {

            "allowed": allowed,

            "reason": reason,

            "regime": regime,

            "volatility": volatility,

        }



    # =====================================================
    # Entry Check
    # =====================================================

    def is_allowed(
        self,
        dataframe: pd.DataFrame,
    ) -> bool:


        return self.evaluate(dataframe)["allowed"]



    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self) -> dict:


        return {

            "checks": self.total_checks,

            "allowed": self.allowed_count,

            "blocked": self.blocked_count,

            "regimes": self.regime_counts,

        }