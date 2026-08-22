"""
Atlas AI Trading Platform 4.2

Adaptive Range Strategy

Designed for:

- sideways markets
- mean reversion
- low trend strength
- Bollinger extremes
- RSI extremes

Atlas 4.2 improvements:

- Separate LONG and SHORT scoring
- Directional mean reversion
- Directional RSI
- ADX range confirmation
- SMA deviation
- Bollinger compression
- Avoids fighting strong trends
"""

from __future__ import annotations

import pandas as pd


class RangeStrategy:

    name = "RangeStrategy"

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
        # ADX RANGE FILTER
        # =====================================================

        if "ADX" in dataframe.columns:

            adx = latest["ADX"]

            if pd.notna(adx):

                adx = float(adx)

                if adx < 20:

                    long_score += 20
                    short_score += 20

                    long_confirmations += 1
                    short_confirmations += 1

                elif adx > 30:

                    return {
                        "signal": "HOLD",
                        "score": 0,
                        "confidence": 0.0,
                        "strategy": self.name,
                    }

        # =====================================================
        # BOLLINGER EXTREMES
        # =====================================================

        if all(
            column in dataframe.columns
            for column in [
                "BB_UPPER",
                "BB_LOWER",
                "BB_MIDDLE",
            ]
        ):

            close = float(latest["Close"])

            upper = latest["BB_UPPER"]
            lower = latest["BB_LOWER"]

            if all(
                pd.notna(value)
                for value in [
                    upper,
                    lower,
                ]
            ):

                if close <= lower:

                    long_score += 35
                    long_confirmations += 1

                elif close >= upper:

                    short_score += 35
                    short_confirmations += 1

        # =====================================================
        # RSI EXTREMES
        # =====================================================

        if "RSI" in dataframe.columns:

            rsi = latest["RSI"]

            if pd.notna(rsi):

                rsi = float(rsi)

                if rsi < 30:

                    long_score += 35
                    long_confirmations += 1

                elif rsi < 40:

                    long_score += 15

                elif rsi > 70:

                    short_score += 35
                    short_confirmations += 1

                elif rsi > 60:

                    short_score += 15

        # =====================================================
        # DISTANCE FROM MEAN
        # =====================================================

        if "SMA_20" in dataframe.columns:

            sma = latest["SMA_20"]
            close = latest["Close"]

            if (
                pd.notna(sma)
                and sma != 0
            ):

                deviation = (
                    (close - sma)
                    / abs(sma)
                    * 100
                )

                if deviation < -2:

                    long_score += 20
                    long_confirmations += 1

                elif deviation > 2:

                    short_score += 20
                    short_confirmations += 1

        # =====================================================
        # BOLLINGER COMPRESSION
        # =====================================================

        if (
            "BB_WIDTH" in dataframe.columns
            and len(dataframe) >= 50
        ):

            current_width = dataframe[
                "BB_WIDTH"
            ].iloc[-1]

            average_width = (
                dataframe["BB_WIDTH"]
                .iloc[-50:]
                .mean()
            )

            if (
                pd.notna(current_width)
                and pd.notna(average_width)
                and current_width < average_width
            ):

                long_score += 5
                short_score += 5

        # =====================================================
        # EMA TREND PROTECTION
        #
        # Do not aggressively fade a strong trend.
        # =====================================================

        if (
            "EMA_20" in dataframe.columns
            and "EMA_50" in dataframe.columns
        ):

            ema20 = latest["EMA_20"]
            ema50 = latest["EMA_50"]
            close = latest["Close"]

            if all(
                pd.notna(value)
                for value in [
                    ema20,
                    ema50,
                    close,
                ]
            ):

                strong_bullish = (
                    close > ema20
                    and ema20 > ema50
                )

                strong_bearish = (
                    close < ema20
                    and ema20 < ema50
                )

                if strong_bullish:

                    short_score -= 20

                elif strong_bearish:

                    long_score -= 20

        # =====================================================
        # FINAL DIRECTION
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
        # CONFIDENCE
        # =====================================================

        if signal != "HOLD":

            confidence = min(
                (
                    score / 100.0
                    + confirmations * 0.04
                ),
                1.0,
            )

            if score < 50:

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