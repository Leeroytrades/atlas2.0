"""
Atlas AI Trading Platform 3.6

Market Regime Detector

Detects:

- Trend
- Range
- Volatility expansion
- Momentum

Used by:

Strategy Router
Backtesting
Walk Forward Validation
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


        result = self.detect()


        return {


            "trend":

                result["trend"],


            "volatility":

                result["volatility"],


            "momentum":

                result["momentum"],


            "regime":

                result["environment"],


            "confidence":

                result["confidence"],

        }



    def detect(self):


        df = self.dataframe



        if df is None or len(df) < 50:


            return {


                "trend":"UNKNOWN",

                "volatility":"UNKNOWN",

                "momentum":"UNKNOWN",

                "environment":"UNKNOWN",

                "confidence":0,

            }



        close = df["Close"]



        # =============================
        # Trend
        # =============================


        ema20 = close.ewm(span=20).mean()

        ema50 = close.ewm(span=50).mean()



        price = close.iloc[-1]



        if price > ema20.iloc[-1] > ema50.iloc[-1]:


            trend="BULLISH"



        elif price < ema20.iloc[-1] < ema50.iloc[-1]:


            trend="BEARISH"



        else:


            trend="SIDEWAYS"



        # =============================
        # Volatility
        # =============================


        volatility="NORMAL"

        expansion=False



        if "ATR" in df.columns:


            atr=df["ATR"].iloc[-1]

            atr_pct=(atr / price) * 100



            if atr_pct > 3:


                volatility="HIGH"



            elif atr_pct < 1:


                volatility="LOW"



        if "BB_WIDTH" in df.columns:


            current=df["BB_WIDTH"].iloc[-1]


            average=(

                df["BB_WIDTH"]

                .rolling(50)

                .mean()

                .iloc[-1]

            )



            if current > average * 1.25:


                expansion=True

                volatility="EXPANDING"



        # =============================
        # Momentum
        # =============================


        if "RSI" in df.columns:


            rsi=df["RSI"].iloc[-1]


            if rsi > 60:


                momentum="POSITIVE"



            elif rsi < 40:


                momentum="NEGATIVE"



            else:


                momentum="NEUTRAL"



        else:


            momentum="UNKNOWN"



        # =============================
        # Environment
        # =============================


        if expansion:


            environment="VOLATILITY"



        elif trend=="SIDEWAYS":


            environment="RANGE"



        else:


            environment="TREND"



        confidence=0.75



        return {


            "trend":trend,

            "volatility":volatility,

            "momentum":momentum,

            "environment":environment,

            "confidence":confidence,

        }