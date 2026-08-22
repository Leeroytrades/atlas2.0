"""
Atlas AI Trading Platform 4.2

Adaptive Volatility Strategy

Designed for:

- volatility expansion
- confirmed breakouts
- momentum continuation
- trend-aligned volatility

Atlas 4.2 improvements:

- Separate LONG and SHORT scoring
- Directional breakout confirmation
- Directional MACD
- Directional EMA alignment
- ATR expansion
- Bollinger expansion
- Volume confirmation
- Anti-chasing filter
- Stronger breakout validation
"""

from __future__ import annotations

import pandas as pd


class VolatilityStrategy:

    name = "VolatilityStrategy"

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
        # PRICE BREAKOUT
        # =====================================================

        recent_high = dataframe[
            "High"
        ].iloc[-20:-1].max()

        recent_low = dataframe[
            "Low"
        ].iloc[-20:-1].min()

        close = float(
            latest["Close"]
        )

        breakout_up = close > recent_high
        breakout_down = close < recent_low

        if breakout_up:

            long_score += 35
            long_confirmations += 1

        elif breakout_down:

            short_score += 35
            short_confirmations += 1

        # =====================================================
        # BOLLINGER EXPANSION
        # =====================================================

        if (
            "BB_WIDTH" in dataframe.columns
            and len(dataframe) >= 20
        ):

            current_width = dataframe[
                "BB_WIDTH"
            ].iloc[-1]

            previous_width = dataframe[
                "BB_WIDTH"
            ].iloc[-2]

            average_width = (
                dataframe["BB_WIDTH"]
                .iloc[-20:]
                .mean()
            )

            if all(
                pd.notna(value)
                for value in [
                    current_width,
                    previous_width,
                    average_width,
                ]
            ):

                # Expansion from a compressed state
                if (
                    current_width > previous_width
                    and current_width < average_width
                ):

                    if breakout_up:

                        long_score += 15
                        long_confirmations += 1

                    elif breakout_down:

                        short_score += 15
                        short_confirmations += 1

                # Strong expansion
                elif current_width > previous_width:

                    if breakout_up:

                        long_score += 10

                    elif breakout_down:

                        short_score += 10

        # =====================================================
        # ATR EXPANSION
        # =====================================================

        if (
            "ATR" in dataframe.columns
            and len(dataframe) >= 2
        ):

            current_atr = dataframe[
                "ATR"
            ].iloc[-1]

            previous_atr = dataframe[
                "ATR"
            ].iloc[-2]

            if (
                pd.notna(current_atr)
                and pd.notna(previous_atr)
                and current_atr > previous_atr
            ):

                if breakout_up:

                    long_score += 10
                    long_confirmations += 1

                elif breakout_down:

                    short_score += 10
                    short_confirmations += 1

        # =====================================================
        # MACD MOMENTUM
        # =====================================================

        if (
            "MACD" in dataframe.columns
            and "MACD_SIGNAL" in dataframe.columns
        ):

            macd = latest["MACD"]
            macd_signal = latest["MACD_SIGNAL"]

            if (
                pd.notna(macd)
                and pd.notna(macd_signal)
            ):

                if (
                    macd > macd_signal
                    and breakout_up
                ):

                    long_score += 15
                    long_confirmations += 1

                elif (
                    macd < macd_signal
                    and breakout_down
                ):

                    short_score += 15
                    short_confirmations += 1

                elif breakout_up:

                    long_score -= 10

                elif breakout_down:

                    short_score -= 10

        # =====================================================
        # EMA ALIGNMENT
        # =====================================================

        if (
            "EMA_20" in dataframe.columns
            and "EMA_50" in dataframe.columns
        ):

            ema20 = latest["EMA_20"]
            ema50 = latest["EMA_50"]

            if (
                pd.notna(ema20)
                and pd.notna(ema50)
            ):

                if (
                    ema20 > ema50
                    and breakout_up
                ):

                    long_score += 15
                    long_confirmations += 1

                elif (
                    ema20 < ema50
                    and breakout_down
                ):

                    short_score += 15
                    short_confirmations += 1

                elif breakout_up:

                    long_score -= 10

                elif breakout_down:

                    short_score -= 10

        # =====================================================
        # EMA200 MACRO FILTER
        # =====================================================

        if "EMA_200" in dataframe.columns:

            ema200 = latest["EMA_200"]

            if pd.notna(ema200):

                if (
                    close > ema200
                    and breakout_up
                ):

                    long_score += 10
                    long_confirmations += 1

                elif (
                    close < ema200
                    and breakout_down
                ):

                    short_score += 10
                    short_confirmations += 1

                elif breakout_up:

                    long_score -= 10

                elif breakout_down:

                    short_score -= 10

        # =====================================================
        # ANTI-CHASING FILTER
        # =====================================================

        if "EMA_20" in dataframe.columns:

            ema20 = latest["EMA_20"]

            if (
                pd.notna(ema20)
                and ema20 != 0
            ):

                distance = (
                    abs(close - ema20)
                    / abs(ema20)
                )

                if distance > 0.06:

                    if breakout_up:

                        long_score -= 20

                    elif breakout_down:

                        short_score -= 20

                elif distance <= 0.03:

                    if breakout_up:

                        long_score += 5

                    elif breakout_down:

                        short_score += 5

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

                if breakout_up:

                    long_score += 10
                    long_confirmations += 1

                elif breakout_down:

                    short_score += 10
                    short_confirmations += 1

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

            if score < 55:

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