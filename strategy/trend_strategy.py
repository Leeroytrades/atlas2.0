"""
Atlas AI Trading Platform 4.6

Institutional Trend Strategy

Entry philosophy:

Trade WITH the trend,
enter ON the pullback,
confirm WITH price and volume.

Returns a normalised signal dictionary.
"""

from __future__ import annotations

import pandas as pd


class TrendStrategy:

    NAME = "TrendStrategy"

    def generate_signal(
        self,
        dataframe: pd.DataFrame,
    ):

        if dataframe is None or len(dataframe) < 220:
            return None

        df = dataframe.copy()

        close = df["Close"]
        high = df["High"]
        low = df["Low"]
        open_ = df["Open"]

        volume = (
            df["Volume"]
            if "Volume" in df.columns
            else pd.Series([0] * len(df))
        )

        ema20 = close.ewm(span=20, adjust=False).mean()
        ema50 = close.ewm(span=50, adjust=False).mean()
        ema200 = close.ewm(span=200, adjust=False).mean()

        delta = close.diff()

        gain = delta.clip(lower=0).rolling(14).mean()
        loss = (-delta.clip(upper=0)).rolling(14).mean()

        rs = gain / loss.replace(0, 1e-9)
        rsi = 100 - (100 / (1 + rs))

        price = close.iloc[-1]

        # =====================================================
        # LONG TREND FILTER
        # =====================================================

        bullish_trend = (
            price > ema200.iloc[-1]
            and ema20.iloc[-1] > ema50.iloc[-1]
            and ema50.iloc[-1] > ema200.iloc[-1]
        )

        bearish_trend = (
            price < ema200.iloc[-1]
            and ema20.iloc[-1] < ema50.iloc[-1]
            and ema50.iloc[-1] < ema200.iloc[-1]
        )

        # =====================================================
        # PULLBACK
        # =====================================================

        pullback_long = (
            low.iloc[-1] <= ema20.iloc[-1] * 1.003
        )

        pullback_short = (
            high.iloc[-1] >= ema20.iloc[-1] * 0.997
        )

        # =====================================================
        # REJECTION CANDLE
        # =====================================================

        bullish_rejection = (
            close.iloc[-1] > open_.iloc[-1]
            and low.iloc[-1] < low.iloc[-2]
        )

        bearish_rejection = (
            close.iloc[-1] < open_.iloc[-1]
            and high.iloc[-1] > high.iloc[-2]
        )

        # =====================================================
        # VOLUME
        # =====================================================

        avg_volume = volume.rolling(20).mean()

        volume_ok = (
            volume.iloc[-1]
            >= avg_volume.iloc[-1]
        )

        # =====================================================
        # RSI
        # =====================================================

        rsi_now = float(rsi.iloc[-1])

        long_momentum = 52 <= rsi_now <= 68
        short_momentum = 32 <= rsi_now <= 48

        # =====================================================
        # BUY
        # =====================================================

        if (
            bullish_trend
            and pullback_long
            and bullish_rejection
            and volume_ok
            and long_momentum
        ):

            score = 60

            score += 10 if rsi_now > 58 else 0
            score += 10 if volume.iloc[-1] > avg_volume.iloc[-1] * 1.2 else 0
            score += 10 if price > ema20.iloc[-1] else 0

            confidence = min(score / 100, 0.95)

            return {
                "signal": "BUY",
                "score": score,
                "confidence": confidence,
                "strategy": self.NAME,
                "reason": "EMA pullback continuation",
            }

        # =====================================================
        # SELL
        # =====================================================

        if (
            bearish_trend
            and pullback_short
            and bearish_rejection
            and volume_ok
            and short_momentum
        ):

            score = 60

            score += 10 if rsi_now < 42 else 0
            score += 10 if volume.iloc[-1] > avg_volume.iloc[-1] * 1.2 else 0
            score += 10 if price < ema20.iloc[-1] else 0

            confidence = min(score / 100, 0.95)

            return {
                "signal": "SELL",
                "score": score,
                "confidence": confidence,
                "strategy": self.NAME,
                "reason": "EMA pullback continuation",
            }

        return None

    # Legacy compatibility
    def generate(self, dataframe):
        return self.generate_signal(dataframe)