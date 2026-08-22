"""
Atlas AI Trading Platform 4.2

Adaptive Trend Strategy

Designed for:

- strong directional markets
- trend continuation
- pullback entries
- momentum confirmation

Atlas 4.2 improvements:

- Separate LONG and SHORT scoring
- Directional RSI confirmation
- Directional pullback confirmation
- Directional MACD confirmation
- EMA200 macro trend confirmation
- ADX trend-strength confirmation
- EMA slope confirmation
- Anti-chasing protection
- Directional volume confirmation
- Cleaner confidence calculation
"""

from __future__ import annotations

import pandas as pd


class TrendStrategy:

    name = "TrendStrategy"

    def generate_signal(
        self,
        dataframe,
    ):

        if dataframe is None or len(dataframe) < 20:

            return {
                "signal": "HOLD",
                "score": 0,
                "confidence": 0.0,
                "strategy": self.name,
            }

        latest = dataframe.iloc[-1]

        long_score = 0
        short_score = 0

        long_confirmations = 0
        short_confirmations = 0

        # =====================================================
        # EMA STRUCTURE
        # =====================================================

        if all(
            column in dataframe.columns
            for column in [
                "EMA_20",
                "EMA_50",
            ]
        ):

            ema20 = float(latest["EMA_20"])
            ema50 = float(latest["EMA_50"])

            if pd.notna(ema20) and pd.notna(ema50):

                if ema20 > ema50:

                    long_score += 25
                    long_confirmations += 1

                elif ema20 < ema50:

                    short_score += 25
                    short_confirmations += 1

        # =====================================================
        # EMA200 MACRO TREND
        # =====================================================

        if "EMA_200" in dataframe.columns:

            price = float(latest["Close"])
            ema200 = float(latest["EMA_200"])

            if pd.notna(ema200):

                if price > ema200:

                    long_score += 20
                    long_confirmations += 1

                elif price < ema200:

                    short_score += 20
                    short_confirmations += 1

        # =====================================================
        # ADX TREND QUALITY
        # =====================================================

        if "ADX" in dataframe.columns:

            adx = latest["ADX"]

            if pd.notna(adx):

                adx = float(adx)

                if adx >= 25:

                    long_score += 15
                    short_score += 15

                    long_confirmations += 1
                    short_confirmations += 1

                elif adx < 15:

                    long_score -= 15
                    short_score -= 15

        # =====================================================
        # EMA SLOPE
        # =====================================================

        if (
            "EMA_20" in dataframe.columns
            and len(dataframe) >= 10
        ):

            current = latest["EMA_20"]
            previous = dataframe["EMA_20"].iloc[-10]

            if (
                pd.notna(current)
                and pd.notna(previous)
            ):

                if current > previous:

                    long_score += 10
                    long_confirmations += 1

                elif current < previous:

                    short_score += 10
                    short_confirmations += 1

        # =====================================================
        # PULLBACK QUALITY
        #
        # A good trend entry should be close to EMA20,
        # but not excessively extended.
        # =====================================================

        if "EMA_20" in dataframe.columns:

            close = float(latest["Close"])
            ema20 = float(latest["EMA_20"])

            if ema20 != 0:

                distance = (
                    abs(close - ema20)
                    / abs(ema20)
                )

                # Price above EMA20 = potential long pullback
                if close >= ema20:

                    if distance <= 0.02:

                        long_score += 15
                        long_confirmations += 1

                    elif distance > 0.06:

                        long_score -= 25

                # Price below EMA20 = potential short pullback
                elif close < ema20:

                    if distance <= 0.02:

                        short_score += 15
                        short_confirmations += 1

                    elif distance > 0.06:

                        short_score -= 25

        # =====================================================
        # MACD MOMENTUM
        # =====================================================

        if all(
            column in dataframe.columns
            for column in [
                "MACD",
                "MACD_SIGNAL",
            ]
        ) and len(dataframe) >= 2:

            macd = latest["MACD"]
            signal = latest["MACD_SIGNAL"]
            previous_macd = dataframe["MACD"].iloc[-2]

            if all(
                pd.notna(value)
                for value in [
                    macd,
                    signal,
                    previous_macd,
                ]
            ):

                # Bullish MACD momentum
                if (
                    macd > signal
                    and macd > previous_macd
                ):

                    long_score += 15
                    long_confirmations += 1

                # Bearish MACD momentum
                elif (
                    macd < signal
                    and macd < previous_macd
                ):

                    short_score += 15
                    short_confirmations += 1

        # =====================================================
        # RSI MOMENTUM
        # =====================================================

        if "RSI" in dataframe.columns:

            rsi = latest["RSI"]

            if pd.notna(rsi):

                rsi = float(rsi)

                # Healthy bullish momentum
                if 52 <= rsi <= 68:

                    long_score += 15
                    long_confirmations += 1

                # Bullish but becoming overextended
                elif 68 < rsi <= 75:

                    long_score += 5

                # Strongly overbought
                elif rsi > 75:

                    long_score -= 20

                # Healthy bearish momentum
                elif 32 <= rsi < 48:

                    short_score += 15
                    short_confirmations += 1

                # Bearish but becoming extended
                elif 25 <= rsi < 32:

                    short_score += 5

                # Strongly oversold
                elif rsi < 25:

                    short_score -= 20

        # =====================================================
        # PRICE MOMENTUM
        # =====================================================

        if len(dataframe) >= 5:

            current_price = float(
                dataframe["Close"].iloc[-1]
            )

            old_price = float(
                dataframe["Close"].iloc[-5]
            )

            if current_price > old_price:

                long_score += 10
                long_confirmations += 1

            elif current_price < old_price:

                short_score += 10
                short_confirmations += 1

        # =====================================================
        # VOLUME CONFIRMATION
        # =====================================================

        if (
            "Volume" in dataframe.columns
            and len(dataframe) >= 20
        ):

            current_volume = latest["Volume"]

            average_volume = (
                dataframe["Volume"]
                .iloc[-20:]
                .mean()
            )

            if (
                pd.notna(current_volume)
                and pd.notna(average_volume)
                and current_volume > average_volume
            ):

                # Volume confirms whichever direction
                # already has the stronger setup.
                if long_score > short_score:

                    long_score += 5
                    long_confirmations += 1

                elif short_score > long_score:

                    short_score += 5
                    short_confirmations += 1

        # =====================================================
        # FINAL DIRECTIONAL SCORE
        # =====================================================

        if long_score > short_score:

            score = long_score
            confirmations = long_confirmations
            signal = "BUY"

        elif short_score > long_score:

            score = short_score
            confirmations = short_confirmations
            signal = "SELL"

        else:

            score = 0
            confirmations = 0
            signal = "HOLD"

        # =====================================================
        # MINIMUM SIGNAL QUALITY
        # =====================================================

        if signal == "BUY":

            confidence = min(
                (
                    score / 100.0
                    + confirmations * 0.04
                ),
                1.0,
            )

            if score < 60:

                signal = "HOLD"

        elif signal == "SELL":

            confidence = min(
                (
                    score / 100.0
                    + confirmations * 0.04
                ),
                1.0,
            )

            if score < 60:

                signal = "HOLD"

        else:

            confidence = 0.0

        # =====================================================
        # RETURN
        # =====================================================

        return {
            "signal": signal,
            "score": int(score),
            "confidence": round(
                confidence,
                3,
            ),
            "strategy": self.name,
        }