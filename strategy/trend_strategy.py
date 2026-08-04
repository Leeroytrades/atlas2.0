"""
Atlas AI Trading Platform 3.5

Trend Strategy

Used when market regime:

- TREND
- BULLISH
- BEARISH

Uses:

EMA structure
MACD
RSI
Momentum confirmation
"""

from __future__ import annotations



class TrendStrategy:



    name = "TrendStrategy"



    def generate_signal(
        self,
        dataframe,
    ):


        latest = dataframe.iloc[-1]


        score = 0



        # -------------------------
        # Trend
        # -------------------------

        if latest["EMA_20"] > latest["EMA_50"]:

            score += 30

        else:

            score -= 30



        # -------------------------
        # Momentum
        # -------------------------

        if latest["MACD"] > latest["MACD_SIGNAL"]:

            score += 25

        else:

            score -= 25



        # -------------------------
        # RSI
        # -------------------------

        if latest["RSI"] > 50:

            score += 20

        elif latest["RSI"] < 40:

            score -= 20



        # -------------------------
        # Volume
        # -------------------------

        if "OBV" in dataframe.columns:

            if latest["OBV"] > dataframe["OBV"].iloc[-2]:

                score += 15



        confidence = min(

            abs(score) / 100,

            1.0

        )



        if score >= 40:

            signal = "BUY"


        elif score <= -40:

            signal = "SELL"


        else:

            signal = "HOLD"



        return {


            "signal":
                signal,


            "score":
                score,


            "confidence":
                confidence,


            "strategy":
                self.name,

        }