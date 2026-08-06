"""
Atlas AI Trading Platform 3.8.2

Trade Quality Filter

Purpose:

Reject poor quality setups before
risk management and execution.

Filters:

- ATR activity
- volume confirmation
- trend clarity
- confidence quality
- overextended entries
"""

from __future__ import annotations


class TradeFilter:


    def __init__(

        self,

        minimum_atr_ratio: float = 0.002,

        minimum_volume_ratio: float = 0.8,

    ):


        self.minimum_atr_ratio = minimum_atr_ratio

        self.minimum_volume_ratio = minimum_volume_ratio



    # =====================================================
    # CHECK TRADE QUALITY
    # =====================================================

    def validate(

        self,

        dataframe,

        signal,

    ):


        latest = dataframe.iloc[-1]



        # -----------------------------------------
        # Confidence filter
        # -----------------------------------------

        confidence = signal.get(

            "confidence",

            0

        )


        if confidence < 0.45:

            return False



        # -----------------------------------------
        # ATR activity filter
        # -----------------------------------------

        if (

            "ATR" in dataframe.columns

            and

            "Close" in dataframe.columns

        ):


            atr = latest["ATR"]

            price = latest["Close"]



            if price > 0:


                atr_ratio = atr / price



                if atr_ratio < self.minimum_atr_ratio:

                    return False



        # -----------------------------------------
        # Volume filter
        # -----------------------------------------

        if "Volume" in dataframe.columns:


            recent_volume = (

                dataframe["Volume"]

                .iloc[-20:]

                .mean()

            )


            current_volume = latest["Volume"]



            if recent_volume > 0:


                volume_ratio = (

                    current_volume /

                    recent_volume

                )


                if volume_ratio < self.minimum_volume_ratio:

                    return False



        # -----------------------------------------
        # Avoid exhaustion entries
        # -----------------------------------------

        if "RSI" in dataframe.columns:


            rsi = latest["RSI"]



            if signal["signal"] == "BUY":


                if rsi > 80:

                    return False



            if signal["signal"] == "SELL":


                if rsi < 20:

                    return False



        return True