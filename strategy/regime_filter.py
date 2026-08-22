"""
Atlas AI Trading Platform 4.3

Adaptive Regime Filter

Determines whether the current market environment contains
enough evidence to permit trading.

Supported regimes:

- BULLISH
- BEARISH
- RANGE
- VOLATILITY
- UNKNOWN

Design goals:

- Reject ambiguous markets.
- Reject weak directional structure.
- Detect genuine trend conditions.
- Detect genuine volatility expansion.
- Detect genuine range conditions.
- Preserve directional information.
- Provide detailed diagnostics.
- Never force UNKNOWN into TREND.
"""

from __future__ import annotations

import pandas as pd

from indicators.composite import build_indicator_set


class RegimeFilter:

    def __init__(
        self,
        allow_ranges: bool = False,
        allow_high_volatility: bool = True,
    ):

        self.allow_ranges = allow_ranges
        self.allow_high_volatility = allow_high_volatility

        self.total_checks = 0
        self.allowed_count = 0
        self.blocked_count = 0

        self.regime_counts = {
            "BULLISH": 0,
            "BEARISH": 0,
            "TREND": 0,
            "RANGE": 0,
            "VOLATILITY": 0,
            "UNKNOWN": 0,
        }

    # =====================================================
    # EVALUATE
    # =====================================================

    def evaluate(
        self,
        dataframe: pd.DataFrame,
    ) -> dict:

        self.total_checks += 1

        # -------------------------------------------------
        # BASIC DATA CHECK
        # -------------------------------------------------

        if (
            dataframe is None
            or not isinstance(dataframe, pd.DataFrame)
            or len(dataframe) < 50
        ):

            return self._blocked_result(
                reason="INSUFFICIENT_DATA"
            )

        dataframe = dataframe.copy()

        # -------------------------------------------------
        # ENSURE INDICATORS EXIST
        # -------------------------------------------------

        required = [
            "EMA_20",
            "EMA_50",
            "ATR",
        ]

        missing = [
            column
            for column in required
            if column not in dataframe.columns
        ]

        if missing:

            try:

                dataframe = build_indicator_set(
                    dataframe
                )

            except Exception:

                return self._blocked_result(
                    reason="INDICATOR_BUILD_FAILED"
                )

        # -------------------------------------------------
        # VERIFY REQUIRED INDICATORS
        # -------------------------------------------------

        missing_after_build = [
            column
            for column in required
            if column not in dataframe.columns
        ]

        if missing_after_build:

            return self._blocked_result(
                reason="MISSING_INDICATORS"
            )

        # -------------------------------------------------
        # LATEST VALUES
        # -------------------------------------------------

        latest = dataframe.iloc[-1]

        try:

            close = float(
                latest["Close"]
            )

            ema20 = float(
                latest["EMA_20"]
            )

            ema50 = float(
                latest["EMA_50"]
            )

            atr = float(
                latest["ATR"]
            )

        except (
            TypeError,
            ValueError,
            KeyError,
        ):

            return self._blocked_result(
                reason="INVALID_MARKET_DATA"
            )

        if (
            pd.isna(close)
            or pd.isna(ema20)
            or pd.isna(ema50)
            or pd.isna(atr)
            or close <= 0
            or ema50 <= 0
            or atr <= 0
        ):

            return self._blocked_result(
                reason="INVALID_MARKET_DATA"
            )

        # =================================================
        # ADX
        # =================================================

        adx = None

        if "ADX" in dataframe.columns:

            value = latest["ADX"]

            if pd.notna(value):

                try:

                    adx = float(value)

                except (
                    TypeError,
                    ValueError,
                ):

                    adx = None

        # =================================================
        # EMA SLOPE
        # =================================================

        ema20_rising = False
        ema20_falling = False

        if len(dataframe) >= 10:

            previous_ema20 = (
                dataframe["EMA_20"]
                .iloc[-10]
            )

            if pd.notna(previous_ema20):

                try:

                    previous_ema20 = float(
                        previous_ema20
                    )

                    ema20_rising = (
                        ema20 > previous_ema20
                    )

                    ema20_falling = (
                        ema20 < previous_ema20
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    pass

        # =================================================
        # EMA GAP
        # =================================================

        ema_gap = (
            abs(
                ema20 - ema50
            )
            /
            abs(ema50)
        )

        # =================================================
        # ATR VOLATILITY
        # =================================================

        atr_series = (
            pd.to_numeric(
                dataframe["ATR"],
                errors="coerce",
            )
            .dropna()
        )

        if len(atr_series) >= 20:

            atr_average = float(
                atr_series
                .iloc[-20:]
                .mean()
            )

        elif len(atr_series) > 0:

            atr_average = float(
                atr_series.mean()
            )

        else:

            atr_average = 0.0

        if atr_average <= 0:

            atr_ratio = 1.0

        else:

            atr_ratio = (
                atr
                /
                atr_average
            )

        if atr_ratio >= 1.25:

            volatility = "HIGH"

        elif atr_ratio <= 0.75:

            volatility = "LOW"

        else:

            volatility = "NORMAL"

        # =================================================
        # BOLLINGER WIDTH
        # =================================================

        bollinger_expanding = False
        bollinger_compressed = False

        if (
            "BB_WIDTH" in dataframe.columns
            and len(dataframe) >= 20
        ):

            widths = pd.to_numeric(
                dataframe["BB_WIDTH"],
                errors="coerce",
            )

            current_width = widths.iloc[-1]
            previous_width = widths.iloc[-2]

            average_width = (
                widths
                .iloc[-20:]
                .mean()
            )

            if (
                pd.notna(current_width)
                and pd.notna(previous_width)
                and pd.notna(average_width)
            ):

                bollinger_expanding = (
                    current_width > previous_width
                    and current_width > average_width
                )

                bollinger_compressed = (
                    current_width
                    <
                    average_width * 0.85
                )

        # =================================================
        # RECENT BREAKOUT
        # =================================================

        breakout_up = False
        breakout_down = False

        if len(dataframe) >= 20:

            recent_high = (
                pd.to_numeric(
                    dataframe["High"],
                    errors="coerce",
                )
                .iloc[-20:-1]
                .max()
            )

            recent_low = (
                pd.to_numeric(
                    dataframe["Low"],
                    errors="coerce",
                )
                .iloc[-20:-1]
                .min()
            )

            if pd.notna(recent_high):

                breakout_up = (
                    close > recent_high
                )

            if pd.notna(recent_low):

                breakout_down = (
                    close < recent_low
                )

        breakout = (
            breakout_up
            or breakout_down
        )

        # =================================================
        # MACRO TREND
        # =================================================

        macro_bullish = False
        macro_bearish = False

        if "EMA_200" in dataframe.columns:

            ema200 = latest["EMA_200"]

            if pd.notna(ema200):

                try:

                    ema200 = float(
                        ema200
                    )

                    macro_bullish = (
                        close > ema200
                    )

                    macro_bearish = (
                        close < ema200
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    pass

        # =================================================
        # DIRECTIONAL STRUCTURE
        # =================================================

        bullish_structure = (
            close > ema20
            and ema20 > ema50
            and ema20_rising
        )

        bearish_structure = (
            close < ema20
            and ema20 < ema50
            and ema20_falling
        )

        # =================================================
        # TREND STRENGTH
        # =================================================

        strong_trend = False

        if adx is not None:

            strong_trend = (
                adx >= 25
            )

        # =================================================
        # VOLATILITY REGIME
        # =================================================

        volatility_regime = False

        if breakout:

            volatility_regime = True

        elif (
            volatility == "HIGH"
            and bollinger_expanding
        ):

            volatility_regime = True

        elif (
            bollinger_expanding
            and strong_trend
        ):

            volatility_regime = True

        # =================================================
        # RANGE CONDITIONS
        # =================================================

        weak_trend = False

        if adx is not None:

            weak_trend = (
                adx < 20
            )

        small_ema_gap = (
            ema_gap < 0.01
        )

        range_structure = (
            weak_trend
            and small_ema_gap
        )

        # =================================================
        # DETERMINE REGIME
        # =================================================

        if volatility_regime:

            regime = "VOLATILITY"

        elif bullish_structure:

            if (
                strong_trend
                or ema_gap >= 0.01
                or macro_bullish
            ):

                regime = "BULLISH"

            else:

                regime = "UNKNOWN"

        elif bearish_structure:

            if (
                strong_trend
                or ema_gap >= 0.01
                or macro_bearish
            ):

                regime = "BEARISH"

            else:

                regime = "UNKNOWN"

        elif range_structure:

            regime = "RANGE"

        else:

            regime = "UNKNOWN"

        # =================================================
        # NORMALISE
        # =================================================

        if regime not in self.regime_counts:

            regime = "UNKNOWN"

        self.regime_counts[regime] += 1

        # =================================================
        # ALLOW / BLOCK
        # =================================================

        allowed = True
        reason = "REGIME_ACCEPTED"

        if regime == "UNKNOWN":

            allowed = False
            reason = "UNKNOWN_REGIME"

        elif regime == "RANGE":

            if self.allow_ranges:

                allowed = True
                reason = "RANGE_ACCEPTED"

            else:

                allowed = False
                reason = "RANGE_BLOCKED"

        elif (
            volatility == "HIGH"
            and not self.allow_high_volatility
        ):

            allowed = False
            reason = "HIGH_VOLATILITY_BLOCKED"

        # =================================================
        # STATISTICS
        # =================================================

        if allowed:

            self.allowed_count += 1

        else:

            self.blocked_count += 1

        # =================================================
        # RETURN
        # =================================================

        return {

            "allowed":
                allowed,

            "reason":
                reason,

            "regime":
                regime,

            "volatility":
                volatility,

            "atr_ratio":
                round(
                    atr_ratio,
                    3,
                ),

            "adx":
                (
                    round(
                        adx,
                        2,
                    )
                    if adx is not None
                    else None
                ),

            "ema_gap":
                round(
                    ema_gap,
                    4,
                ),

            "breakout":
                breakout,

            "breakout_up":
                breakout_up,

            "breakout_down":
                breakout_down,

            "bollinger_expanding":
                bollinger_expanding,

            "bollinger_compressed":
                bollinger_compressed,

            "bullish_structure":
                bullish_structure,

            "bearish_structure":
                bearish_structure,

            "strong_trend":
                strong_trend,

            "macro_bullish":
                macro_bullish,

            "macro_bearish":
                macro_bearish,
        }

    # =====================================================
    # BLOCKED RESULT
    # =====================================================

    def _blocked_result(
        self,
        reason: str,
    ) -> dict:

        self.blocked_count += 1

        self.regime_counts["UNKNOWN"] += 1

        return {

            "allowed":
                False,

            "reason":
                reason,

            "regime":
                "UNKNOWN",

            "volatility":
                "UNKNOWN",

            "atr_ratio":
                None,

            "adx":
                None,

            "ema_gap":
                None,

            "breakout":
                False,

            "breakout_up":
                False,

            "breakout_down":
                False,

            "bollinger_expanding":
                False,

            "bollinger_compressed":
                False,

            "bullish_structure":
                False,

            "bearish_structure":
                False,

            "strong_trend":
                False,

            "macro_bullish":
                False,

            "macro_bearish":
                False,
        }

    # =====================================================
    # ENTRY CHECK
    # =====================================================

    def is_allowed(
        self,
        dataframe: pd.DataFrame,
    ) -> bool:

        return bool(
            self.evaluate(
                dataframe
            ).get(
                "allowed",
                False,
            )
        )

    # =====================================================
    # STATISTICS
    # =====================================================

    def statistics(self) -> dict:

        return {

            "checks":
                self.total_checks,

            "allowed":
                self.allowed_count,

            "blocked":
                self.blocked_count,

            "regimes":
                self.regime_counts.copy(),

        }