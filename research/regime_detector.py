"""
Atlas AI Trading Platform 3.3

Market Regime Detector

Compatible with Atlas
Walk Forward Validation.

Detects:

- Trend
- Volatility
- Momentum
- Environment
"""

from __future__ import annotations



class RegimeDetector:


    def __init__(
        self,
        dataframe=None,
    ):

        self.dataframe = dataframe



    def analyse(
        self,
        dataframe,
    ):

        self.dataframe = dataframe

        regime = self.detect()


        return {

            "trend":
                regime["trend"],

            "volatility":
                regime["volatility"],

            "momentum":
                regime["momentum"],

            "regime":
                regime["environment"],

        }



    def detect(
        self,
    ):


        df = self.dataframe


        if df is None or len(df) < 50:

            return {

                "trend":
                    "UNKNOWN",

                "volatility":
                    "UNKNOWN",

                "momentum":
                    "UNKNOWN",

                "environment":
                    "UNKNOWN",

            }



        close = df["Close"]



        # -----------------------------
        # Trend
        # -----------------------------


        ema20 = (
            close
            .ewm(
                span=20
            )
            .mean()
        )


        ema50 = (
            close
            .ewm(
                span=50
            )
            .mean()
        )


        price = close.iloc[-1]



        if price > ema20.iloc[-1] > ema50.iloc[-1]:

            trend = "BULLISH"


        elif price < ema20.iloc[-1] < ema50.iloc[-1]:

            trend = "BEARISH"


        else:

            trend = "SIDEWAYS"



        # -----------------------------
        # Volatility
        # -----------------------------


        if "ATR" in df.columns:


            atr = float(
                df["ATR"].iloc[-1]
            )


            atr_percent = (

                atr

                /

                price

                *

                100

            )


            if atr_percent > 3:

                volatility = "HIGH"


            elif atr_percent < 1:

                volatility = "LOW"


            else:

                volatility = "NORMAL"


        else:

            volatility = "UNKNOWN"



        # -----------------------------
        # Momentum
        # -----------------------------


        if "RSI" in df.columns:


            rsi = float(
                df["RSI"].iloc[-1]
            )


            if rsi > 60:

                momentum = "POSITIVE"


            elif rsi < 40:

                momentum = "NEGATIVE"


            else:

                momentum = "NEUTRAL"


        else:

            momentum = "UNKNOWN"



        # -----------------------------
        # Environment
        # -----------------------------


        if trend == "SIDEWAYS":

            environment = "RANGE"


        elif volatility == "HIGH":

            environment = "VOLATILE TREND"


        else:

            environment = "TREND"



        return {

            "trend":
                trend,

            "volatility":
                volatility,

            "momentum":
                momentum,

            "environment":
                environment,

        }