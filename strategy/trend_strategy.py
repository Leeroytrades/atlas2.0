"""
Atlas AI Trading Platform 4.1

Adaptive Trend Strategy

Designed for:

- strong directional markets
- trend continuation
- pullback entries
- momentum confirmation

Uses:

- EMA structure
- EMA200 macro trend
- ADX strength
- EMA slope
- MACD momentum
- RSI momentum
- Pullback quality
- Volume confirmation
- Trend persistence

Improvements from 3.9:

- fewer weak entries
- avoids late trend chasing
- stronger continuation setups
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


        confirmations = 0



        # =====================================================
        # EMA STRUCTURE
        # =====================================================

        if all(

            col in dataframe.columns

            for col in [

                "EMA_20",

                "EMA_50",

            ]

        ):


            ema20 = latest["EMA_20"]

            ema50 = latest["EMA_50"]



            if ema20 > ema50:


                score += 30

                confirmations += 1



            elif ema20 < ema50:


                score -= 30

                confirmations += 1




        # =====================================================
        # MACRO TREND FILTER
        # =====================================================

        if "EMA_200" in dataframe.columns:


            price = latest["Close"]

            ema200 = latest["EMA_200"]



            if price > ema200:


                score += 20



            else:


                score -= 20




        # =====================================================
        # ADX TREND QUALITY
        # =====================================================

        if "ADX" in dataframe.columns:


            adx = latest["ADX"]



            if adx >= 25:


                score += 20

                confirmations += 1



            elif adx < 15:


                score -= 15




        # =====================================================
        # EMA SLOPE
        # =====================================================

        if (

            "EMA_20" in dataframe.columns

            and

            len(dataframe) >= 10

        ):


            old = dataframe["EMA_20"].iloc[-10]

            current = latest["EMA_20"]



            if current > old:


                score += 10



            elif current < old:


                score -= 10




        # =====================================================
        # PULLBACK QUALITY
        # =====================================================

        if "EMA_20" in dataframe.columns:


            close = latest["Close"]

            ema20 = latest["EMA_20"]



            distance = abs(close - ema20) / ema20



            if distance < 0.02:


                score += 15

                confirmations += 1



            elif distance > 0.06:


                score -= 25




        # =====================================================
        # MACD MOMENTUM
        # =====================================================

        if all(

            col in dataframe.columns

            for col in [

                "MACD",

                "MACD_SIGNAL",

            ]

        ):


            macd = latest["MACD"]

            signal = latest["MACD_SIGNAL"]



            previous_macd = dataframe["MACD"].iloc[-2]



            if (

                macd > signal

                and

                macd > previous_macd

            ):


                score += 20



            elif (

                macd < signal

                and

                macd < previous_macd

            ):


                score -= 20




        # =====================================================
        # RSI MOMENTUM FILTER
        # =====================================================

        if "RSI" in dataframe.columns:


            rsi = latest["RSI"]



            if 52 <= rsi <= 68:


                score += 15



            elif rsi > 75:


                score -= 20



            elif rsi < 35:


                score -= 10




        # =====================================================
        # PRICE MOMENTUM
        # =====================================================

        if len(dataframe) >= 5:


            old_price = dataframe["Close"].iloc[-5]

            current_price = latest["Close"]



            if current_price > old_price:


                score += 10



            else:


                score -= 10




        # =====================================================
        # VOLUME CONFIRMATION
        # =====================================================

        if (

            "Volume" in dataframe.columns

            and

            len(dataframe) >= 20

        ):


            average_volume = (

                dataframe["Volume"]

                .iloc[-20:]

                .mean()

            )


            if latest["Volume"] > average_volume:


                score += 5




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

        if score >= 60:


            signal = "BUY"



        elif score <= -60:


            signal = "SELL"



        else:


            signal = "HOLD"




        return {


            "signal": signal,


            "score": score,


            "confidence": round(confidence, 3),


            "strategy": self.name,

        }