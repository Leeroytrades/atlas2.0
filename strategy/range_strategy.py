"""
Atlas AI Trading Platform 4.0

Enhanced Range Strategy

Designed for:

- Sideways markets
- Mean reversion
- Low trend strength environments

Uses:

- Bollinger Bands
- RSI extremes
- SMA deviation
- ADX filter
- Bollinger compression
- Mean reversion probability

Changes from 3.x:

- Avoids fighting strong trends
- Requires multiple oversold/overbought confirmations
- Reduces false range entries
- Stronger confidence scoring
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


        confirmations = 0



        # =====================================================
        # ADX RANGE FILTER
        # =====================================================

        if "ADX" in dataframe.columns:


            adx = latest["ADX"]


            if adx < 20:

                score += 25

                confirmations += 1


            elif adx > 30:

                score -= 40




        # =====================================================
        # BOLLINGER MEAN REVERSION
        # =====================================================

        if all(

            column in dataframe.columns

            for column in [

                "BB_UPPER",

                "BB_LOWER",

                "BB_MIDDLE",

            ]

        ):


            close = latest["Close"]


            upper = latest["BB_UPPER"]

            lower = latest["BB_LOWER"]

            middle = latest["BB_MIDDLE"]



            if close <= lower:


                score += 35

                confirmations += 1



            elif close >= upper:


                score -= 35

                confirmations += 1



            elif close < middle:


                score += 10



            elif close > middle:


                score -= 10




        # =====================================================
        # RSI EXTREMES
        # =====================================================

        if "RSI" in dataframe.columns:


            rsi = latest["RSI"]



            if rsi < 30:


                score += 35

                confirmations += 1



            elif rsi < 40:


                score += 15



            elif rsi > 70:


                score -= 35

                confirmations += 1



            elif rsi > 60:


                score -= 15




        # =====================================================
        # DISTANCE FROM MEAN
        # =====================================================

        if "SMA_20" in dataframe.columns:


            sma = latest["SMA_20"]


            close = latest["Close"]



            if sma != 0:


                deviation = (

                    (close - sma)

                    /

                    sma

                    *

                    100

                )



                if deviation < -2:


                    score += 20



                elif deviation > 2:


                    score -= 20




        # =====================================================
        # VOLATILITY COMPRESSION
        # =====================================================

        if "BB_WIDTH" in dataframe.columns:


            current_width = latest["BB_WIDTH"]



            average_width = (

                dataframe["BB_WIDTH"]

                .rolling(50)

                .mean()

                .iloc[-1]

            )



            if current_width < average_width:


                score += 10




        # =====================================================
        # CONFIDENCE
        # =====================================================

        confidence = min(

            (

                abs(score) / 100

                +

                confirmations * 0.05

            ),

            1.0

        )



        # =====================================================
        # SIGNAL
        # =====================================================

        if score >= 50:


            signal = "BUY"



        elif score <= -50:


            signal = "SELL"



        else:


            signal = "HOLD"




        return {


            "signal": signal,


            "score": score,


            "confidence": round(confidence, 3),


            "strategy": self.name,

        }