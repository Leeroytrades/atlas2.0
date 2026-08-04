"""
Atlas AI Trading Platform 3.5

Range Strategy

Designed for:

- Sideways markets
- Mean reversion
- Low volatility environments

Uses:

- Bollinger Bands
- RSI extremes
- Price deviation
"""

from __future__ import annotations



class RangeStrategy:


    name = "RangeStrategy"



    def generate_signal(
        self,
        dataframe,
    ):


        latest = dataframe.iloc[-1]


        score = 0



        # -------------------------
        # Bollinger mean reversion
        # -------------------------

        if "BB_LOW" in dataframe.columns:


            if latest["Close"] <= latest["BB_LOW"]:

                score += 35



        if "BB_HIGH" in dataframe.columns:


            if latest["Close"] >= latest["BB_HIGH"]:

                score -= 35



        # -------------------------
        # RSI extremes
        # -------------------------

        if latest["RSI"] < 35:

            score += 30


        elif latest["RSI"] > 65:

            score -= 30



        # -------------------------
        # Volatility confirmation
        # -------------------------

        if "BB_WIDTH" in dataframe.columns:


            width = latest["BB_WIDTH"]


            if width < dataframe["BB_WIDTH"].mean():

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