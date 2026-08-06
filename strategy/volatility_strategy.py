"""
Atlas AI Trading Platform 4.1

Adaptive Volatility Strategy

Designed for:

- volatility expansion
- confirmed breakouts
- momentum continuation
- trend aligned volatility

Features:

- breakout validation
- Bollinger squeeze detection
- ATR expansion
- MACD momentum
- EMA alignment
- volume confirmation
- anti-chasing filter
"""

from __future__ import annotations



class VolatilityStrategy:


    name = "VolatilityStrategy"



    def generate_signal(
        self,
        dataframe,
    ):


        latest = dataframe.iloc[-1]


        score = 0

        confirmations = 0



        # =====================================================
        # PRICE BREAKOUT
        # =====================================================

        if len(dataframe) >= 20:


            recent_high = dataframe["High"].iloc[-20:-1].max()

            recent_low = dataframe["Low"].iloc[-20:-1].min()


            close = latest["Close"]



            if close > recent_high:


                score += 35

                confirmations += 1



            elif close < recent_low:


                score -= 35

                confirmations += 1




        # =====================================================
        # BOLLINGER SQUEEZE -> EXPANSION
        # =====================================================

        if (

            "BB_WIDTH" in dataframe.columns

            and len(dataframe) >= 20

        ):


            current_width = latest["BB_WIDTH"]


            average_width = (

                dataframe["BB_WIDTH"]

                .iloc[-20:]

                .mean()

            )


            previous_width = dataframe["BB_WIDTH"].iloc[-2]



            if (

                current_width > previous_width

                and

                current_width < average_width

            ):


                score += 15

                confirmations += 1



            elif current_width > previous_width:


                score += 5




        # =====================================================
        # ATR EXPANSION
        # =====================================================

        if "ATR" in dataframe.columns:


            current_atr = latest["ATR"]

            previous_atr = dataframe["ATR"].iloc[-2]



            if current_atr > previous_atr:


                score += 10

                confirmations += 1




        # =====================================================
        # MACD MOMENTUM
        # =====================================================

        if (

            "MACD" in dataframe.columns

            and

            "MACD_SIGNAL" in dataframe.columns

        ):


            if latest["MACD"] > latest["MACD_SIGNAL"]:


                score += 15



            else:


                score -= 15




        # =====================================================
        # TREND ALIGNMENT
        # =====================================================

        if (

            "EMA_20" in dataframe.columns

            and

            "EMA_50" in dataframe.columns

        ):


            if latest["EMA_20"] > latest["EMA_50"]:


                score += 15



            else:


                score -= 15




        # =====================================================
        # OVEREXTENSION FILTER
        # =====================================================

        if "EMA_20" in dataframe.columns:


            distance = (

                abs(

                    latest["Close"]

                    -

                    latest["EMA_20"]

                )

                /

                latest["EMA_20"]

            )



            if distance > 0.06:


                score -= 15




        # =====================================================
        # VOLUME CONFIRMATION
        # =====================================================

        if (

            "Volume" in dataframe.columns

            and len(dataframe) >= 20

        ):


            average_volume = (

                dataframe["Volume"]

                .iloc[-20:]

                .mean()

            )


            if latest["Volume"] > average_volume:


                score += 10

                confirmations += 1




        # =====================================================
        # CONFIDENCE
        # =====================================================

        confidence = min(

            abs(score) / 100

            +

            confirmations * 0.05,

            1.0

        )




        # =====================================================
        # SIGNAL
        # =====================================================

        if score >= 55:


            signal = "BUY"



        elif score <= -55:


            signal = "SELL"



        else:


            signal = "HOLD"




        return {


            "signal": signal,


            "score": score,


            "confidence": round(confidence, 3),


            "strategy": self.name,

        }