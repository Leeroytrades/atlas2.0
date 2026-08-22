
"""
Atlas AI Trading Platform 3.6

Market Regime Detector

Detects:

- Bullish trend
- Bearish trend
- Range / sideways market
- Volatility expansion
- Momentum
- Breakouts
- Trend strength
- Market structure
- Macro trend structure

Designed for use by:

- Strategy Router
- Backtesting
- Walk Forward Validation
- Strategy Optimisation

The detector deliberately returns a stable schema so that all
downstream modules receive consistent regime information.
"""

from __future__ import annotations

from typing import Any, Dict

import numpy as np
import pandas as pd


class RegimeDetector:
    """
    Detect the current market regime from OHLCV/indicator data.

    Returned regime values:

        BULLISH
        BEARISH
        RANGE
        VOLATILITY
        UNKNOWN

    The detector is intentionally defensive. Missing indicators do not
    automatically cause the whole regime calculation to fail.
    """

    def __init__(self, dataframe: pd.DataFrame | None = None):
        self.dataframe = dataframe

    # ------------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------------

    def analyse(
        self,
        dataframe: pd.DataFrame | None = None,
    ) -> Dict[str, Any]:
        """
        Analyse the supplied dataframe.

        Returns a stable dictionary consumed by the Strategy Router,
        Backtester and Walk Forward Validator.
        """

        if dataframe is not None:
            self.dataframe = dataframe

        result = self.detect()

        return {
            "trend": result["trend"],
            "volatility": result["volatility"],
            "momentum": result["momentum"],
            "regime": result["regime"],
            "environment": result["environment"],
            "confidence": result["confidence"],
            "allowed": result["allowed"],
            "reason": result["reason"],
            "atr_ratio": result["atr_ratio"],
            "adx": result["adx"],
            "ema_gap": result["ema_gap"],
            "breakout": result["breakout"],
            "breakout_up": result["breakout_up"],
            "breakout_down": result["breakout_down"],
            "bollinger_expanding": result["bollinger_expanding"],
            "bullish_structure": result["bullish_structure"],
            "bearish_structure": result["bearish_structure"],
            "strong_trend": result["strong_trend"],
            "macro_bullish": result["macro_bullish"],
            "macro_bearish": result["macro_bearish"],
        }

    # ------------------------------------------------------------------
    # MAIN DETECTOR
    # ------------------------------------------------------------------

    def detect(self) -> Dict[str, Any]:
        df = self.dataframe

        if df is None or len(df) < 50:
            return self._unknown_result(
                reason="INSUFFICIENT_DATA"
            )

        df = self._prepare_dataframe(df)

        if df is None or len(df) < 50:
            return self._unknown_result(
                reason="INSUFFICIENT_DATA"
            )

        close = self._series(df, "Close")

        if close is None:
            return self._unknown_result(
                reason="MISSING_CLOSE"
            )

        price = self._safe_float(close.iloc[-1])

        if price is None or price <= 0:
            return self._unknown_result(
                reason="INVALID_PRICE"
            )

        # ==============================================================
        # CORE INDICATORS
        # ==============================================================

        ema20 = close.ewm(
            span=20,
            adjust=False,
            min_periods=20,
        ).mean()

        ema50 = close.ewm(
            span=50,
            adjust=False,
            min_periods=50,
        ).mean()

        ema200 = close.ewm(
            span=200,
            adjust=False,
            min_periods=min(200, len(close)),
        ).mean()

        ema20_now = self._safe_float(ema20.iloc[-1])
        ema50_now = self._safe_float(ema50.iloc[-1])
        ema200_now = self._safe_float(ema200.iloc[-1])

        # ==============================================================
        # EMA GAP
        # ==============================================================

        ema_gap = 0.0

        if (
            ema20_now is not None
            and ema50_now is not None
            and ema50_now != 0
        ):
            ema_gap = abs(
                (ema20_now - ema50_now)
                / ema50_now
            )

        # ==============================================================
        # ATR / VOLATILITY
        # ==============================================================

        atr = self._get_atr(df)

        atr_ratio = 1.0

        if atr is not None and atr > 0:
            atr_ratio = atr / price * 100.0

        volatility = self._detect_volatility(
            df=df,
            atr_ratio=atr_ratio,
        )

        # ==============================================================
        # ADX
        # ==============================================================

        adx = self._get_adx(df)

        if adx is None:
            adx = 0.0

        strong_trend = adx >= 25.0

        # ==============================================================
        # RSI / MOMENTUM
        # ==============================================================

        rsi = self._get_rsi(df)

        if rsi is None:
            momentum = "UNKNOWN"
        elif rsi >= 60:
            momentum = "POSITIVE"
        elif rsi <= 40:
            momentum = "NEGATIVE"
        else:
            momentum = "NEUTRAL"

        # ==============================================================
        # MARKET STRUCTURE
        # ==============================================================

        bullish_structure = self._bullish_structure(df)

        bearish_structure = self._bearish_structure(df)

        # ==============================================================
        # MACRO STRUCTURE
        # ==============================================================

        macro_bullish = False
        macro_bearish = False

        if ema200_now is not None:
            macro_bullish = (
                price > ema200_now
                and ema50_now is not None
                and ema50_now > ema200_now
            )

            macro_bearish = (
                price < ema200_now
                and ema50_now is not None
                and ema50_now < ema200_now
            )

        # ==============================================================
        # BREAKOUT
        # ==============================================================

        breakout_up, breakout_down = self._detect_breakout(df)

        breakout = breakout_up or breakout_down

        # ==============================================================
        # TREND CLASSIFICATION
        # ==============================================================

        bullish_score = 0
        bearish_score = 0

        # Price / EMA structure
        if (
            ema20_now is not None
            and ema50_now is not None
        ):
            if price > ema20_now > ema50_now:
                bullish_score += 2

            elif price < ema20_now < ema50_now:
                bearish_score += 2

        # EMA slope
        if len(ema20) >= 5:
            ema20_previous = self._safe_float(
                ema20.iloc[-5]
            )

            if (
                ema20_previous is not None
                and ema20_now is not None
            ):
                if ema20_now > ema20_previous:
                    bullish_score += 1

                elif ema20_now < ema20_previous:
                    bearish_score += 1

        # Market structure
        if bullish_structure:
            bullish_score += 2

        if bearish_structure:
            bearish_score += 2

        # Macro structure
        if macro_bullish:
            bullish_score += 2

        if macro_bearish:
            bearish_score += 2

        # Breakout direction
        if breakout_up:
            bullish_score += 2

        if breakout_down:
            bearish_score += 2

        # ==============================================================
        # TREND RESULT
        # ==============================================================

        if bullish_score >= 3 and bullish_score > bearish_score:
            trend = "BULLISH"

        elif bearish_score >= 3 and bearish_score > bullish_score:
            trend = "BEARISH"

        else:
            trend = "SIDEWAYS"

        # ==============================================================
        # ENVIRONMENT / REGIME
        # ==============================================================

        # Volatility expansion gets priority because a breakout/
        # expansion environment should not be incorrectly classified
        # simply as a normal trend.
        if volatility == "EXPANDING":
            regime = "VOLATILITY"

        elif volatility == "HIGH" and breakout:
            regime = "VOLATILITY"

        elif trend == "BULLISH":
            regime = "BULLISH"

        elif trend == "BEARISH":
            regime = "BEARISH"

        elif trend == "SIDEWAYS":
            regime = "RANGE"

        else:
            regime = "UNKNOWN"

        environment = regime

        # ==============================================================
        # CONFIDENCE
        # ==============================================================

        confidence = self._calculate_confidence(
            trend=trend,
            regime=regime,
            adx=adx,
            ema_gap=ema_gap,
            bullish_structure=bullish_structure,
            bearish_structure=bearish_structure,
            macro_bullish=macro_bullish,
            macro_bearish=macro_bearish,
            breakout=breakout,
            volatility=volatility,
            momentum=momentum,
        )

        # ==============================================================
        # REGIME ACCEPTANCE
        # ==============================================================

        allowed, reason = self._regime_allowed(
            regime=regime,
            confidence=confidence,
            adx=adx,
            breakout=breakout,
            volatility=volatility,
            trend=trend,
        )

        return {
            "trend": trend,
            "volatility": volatility,
            "momentum": momentum,
            "regime": regime,
            "environment": environment,
            "confidence": round(confidence, 2),
            "allowed": allowed,
            "reason": reason,
            "atr_ratio": round(atr_ratio, 3),
            "adx": round(adx, 2),
            "ema_gap": round(ema_gap, 4),
            "breakout": bool(breakout),
            "breakout_up": bool(breakout_up),
            "breakout_down": bool(breakout_down),
            "bollinger_expanding": bool(
                self._bollinger_expanding(df)
            ),
            "bullish_structure": bool(
                bullish_structure
            ),
            "bearish_structure": bool(
                bearish_structure
            ),
            "strong_trend": bool(strong_trend),
            "macro_bullish": bool(macro_bullish),
            "macro_bearish": bool(macro_bearish),
        }

    # ------------------------------------------------------------------
    # DATA PREPARATION
    # ------------------------------------------------------------------

    def _prepare_dataframe(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame | None:

        if dataframe is None:
            return None

        df = dataframe.copy()

        # Normalise common column naming issues.
        rename_map = {}

        for column in df.columns:
            name = str(column).strip()

            if name.lower() == "close":
                rename_map[column] = "Close"

            elif name.lower() == "high":
                rename_map[column] = "High"

            elif name.lower() == "low":
                rename_map[column] = "Low"

            elif name.lower() == "open":
                rename_map[column] = "Open"

            elif name.lower() == "volume":
                rename_map[column] = "Volume"

        if rename_map:
            df = df.rename(columns=rename_map)

        return df

    # ------------------------------------------------------------------
    # SERIES HELPERS
    # ------------------------------------------------------------------

    @staticmethod
    def _series(
        df: pd.DataFrame,
        name: str,
    ) -> pd.Series | None:

        if name not in df.columns:
            return None

        series = pd.to_numeric(
            df[name],
            errors="coerce",
        )

        return series

    @staticmethod
    def _safe_float(value) -> float | None:

        try:
            value = float(value)

            if not np.isfinite(value):
                return None

            return value

        except (
            TypeError,
            ValueError,
        ):
            return None

    # ------------------------------------------------------------------
    # ATR
    # ------------------------------------------------------------------

    def _get_atr(
        self,
        df: pd.DataFrame,
    ) -> float | None:

        if "ATR" in df.columns:
            value = self._safe_float(
                pd.to_numeric(
                    df["ATR"],
                    errors="coerce",
                ).iloc[-1]
            )

            if value is not None and value > 0:
                return value

        high = self._series(df, "High")
        low = self._series(df, "Low")
        close = self._series(df, "Close")

        if (
            high is None
            or low is None
            or close is None
        ):
            return None

        previous_close = close.shift(1)

        true_range = pd.concat(
            [
                high - low,
                (high - previous_close).abs(),
                (low - previous_close).abs(),
            ],
            axis=1,
        ).max(axis=1)

        atr = true_range.rolling(
            14,
            min_periods=14,
        ).mean()

        return self._safe_float(
            atr.iloc[-1]
        )

    # ------------------------------------------------------------------
    # ADX
    # ------------------------------------------------------------------

    def _get_adx(
        self,
        df: pd.DataFrame,
    ) -> float | None:

        if "ADX" in df.columns:
            return self._safe_float(
                pd.to_numeric(
                    df["ADX"],
                    errors="coerce",
                ).iloc[-1]
            )

        high = self._series(df, "High")
        low = self._series(df, "Low")
        close = self._series(df, "Close")

        if (
            high is None
            or low is None
            or close is None
        ):
            return None

        up_move = high.diff()
        down_move = -low.diff()

        plus_dm = pd.Series(
            np.where(
                (up_move > down_move)
                & (up_move > 0),
                up_move,
                0.0,
            ),
            index=df.index,
        )

        minus_dm = pd.Series(
            np.where(
                (down_move > up_move)
                & (down_move > 0),
                down_move,
                0.0,
            ),
            index=df.index,
        )

        previous_close = close.shift(1)

        tr = pd.concat(
            [
                high - low,
                (high - previous_close).abs(),
                (low - previous_close).abs(),
            ],
            axis=1,
        ).max(axis=1)

        atr = tr.rolling(
            14,
            min_periods=14,
        ).mean()

        plus_di = (
            100
            * plus_dm.rolling(
                14,
                min_periods=14,
            ).mean()
            / atr.replace(0, np.nan)
        )

        minus_di = (
            100
            * minus_dm.rolling(
                14,
                min_periods=14,
            ).mean()
            / atr.replace(0, np.nan)
        )

        denominator = (
            plus_di + minus_di
        ).replace(0, np.nan)

        dx = (
            100
            * (plus_di - minus_di).abs()
            / denominator
        )

        adx = dx.rolling(
            14,
            min_periods=14,
        ).mean()

        return self._safe_float(
            adx.iloc[-1]
        )

    # ------------------------------------------------------------------
    # RSI
    # ------------------------------------------------------------------

    def _get_rsi(
        self,
        df: pd.DataFrame,
    ) -> float | None:

        if "RSI" in df.columns:
            return self._safe_float(
                pd.to_numeric(
                    df["RSI"],
                    errors="coerce",
                ).iloc[-1]
            )

        close = self._series(df, "Close")

        if close is None:
            return None

        delta = close.diff()

        gain = delta.clip(
            lower=0
        )

        loss = -delta.clip(
            upper=0
        )

        average_gain = gain.rolling(
            14,
            min_periods=14,
        ).mean()

        average_loss = loss.rolling(
            14,
            min_periods=14,
        ).mean()

        rs = (
            average_gain
            / average_loss.replace(
                0,
                np.nan,
            )
        )

        rsi = 100 - (
            100 / (1 + rs)
        )

        return self._safe_float(
            rsi.iloc[-1]
        )

    # ------------------------------------------------------------------
    # VOLATILITY
    # ------------------------------------------------------------------

    def _detect_volatility(
        self,
        df: pd.DataFrame,
        atr_ratio: float,
    ) -> str:

        volatility = "NORMAL"

        if atr_ratio >= 3.0:
            volatility = "HIGH"

        elif atr_ratio <= 1.0:
            volatility = "LOW"

        if self._bollinger_expanding(df):
            volatility = "EXPANDING"

        return volatility

    def _bollinger_expanding(
        self,
        df: pd.DataFrame,
    ) -> bool:

        if "BB_WIDTH" in df.columns:

            width = pd.to_numeric(
                df["BB_WIDTH"],
                errors="coerce",
            )

        else:

            close = self._series(
                df,
                "Close",
            )

            if close is None:
                return False

            middle = close.rolling(
                20,
                min_periods=20,
            ).mean()

            std = close.rolling(
                20,
                min_periods=20,
            ).std()

            width = (
                4 * std / middle.replace(
                    0,
                    np.nan,
                )
            )

        if len(width.dropna()) < 50:
            return False

        current = self._safe_float(
            width.iloc[-1]
        )

        average = self._safe_float(
            width.rolling(
                50,
                min_periods=50,
            ).mean().iloc[-1]
        )

        if (
            current is None
            or average is None
            or average <= 0
        ):
            return False

        return current > average * 1.20

    # ------------------------------------------------------------------
    # MARKET STRUCTURE
    # ------------------------------------------------------------------

    def _bullish_structure(
        self,
        df: pd.DataFrame,
    ) -> bool:

        high = self._series(df, "High")
        low = self._series(df, "Low")

        if high is None or low is None:
            return False

        if len(df) < 30:
            return False

        recent_high = high.iloc[-10:].max()
        previous_high = high.iloc[-20:-10].max()

        recent_low = low.iloc[-10:].min()
        previous_low = low.iloc[-20:-10].min()

        return (
            recent_high > previous_high
            and recent_low > previous_low
        )

    def _bearish_structure(
        self,
        df: pd.DataFrame,
    ) -> bool:

        high = self._series(df, "High")
        low = self._series(df, "Low")

        if high is None or low is None:
            return False

        if len(df) < 30:
            return False

        recent_high = high.iloc[-10:].max()
        previous_high = high.iloc[-20:-10].max()

        recent_low = low.iloc[-10:].min()
        previous_low = low.iloc[-20:-10].min()

        return (
            recent_high < previous_high
            and recent_low < previous_low
        )

    # ------------------------------------------------------------------
    # BREAKOUT
    # ------------------------------------------------------------------

    def _detect_breakout(
        self,
        df: pd.DataFrame,
    ) -> tuple[bool, bool]:

        high = self._series(df, "High")
        low = self._series(df, "Low")
        close = self._series(df, "Close")

        if (
            high is None
            or low is None
            or close is None
            or len(df) < 22
        ):
            return False, False

        previous_high = high.iloc[-21:-1].max()
        previous_low = low.iloc[-21:-1].min()

        current_close = close.iloc[-1]

        breakout_up = (
            current_close > previous_high
        )

        breakout_down = (
            current_close < previous_low
        )

        return (
            bool(breakout_up),
            bool(breakout_down),
        )

    # ------------------------------------------------------------------
    # CONFIDENCE
    # ------------------------------------------------------------------

    def _calculate_confidence(
        self,
        trend: str,
        regime: str,
        adx: float,
        ema_gap: float,
        bullish_structure: bool,
        bearish_structure: bool,
        macro_bullish: bool,
        macro_bearish: bool,
        breakout: bool,
        volatility: str,
        momentum: str,
    ) -> float:

        confidence = 0.50

        # Strong ADX
        if adx >= 35:
            confidence += 0.15

        elif adx >= 25:
            confidence += 0.10

        # EMA separation
        if ema_gap >= 0.02:
            confidence += 0.10

        elif ema_gap >= 0.01:
            confidence += 0.05

        # Structure
        if bullish_structure or bearish_structure:
            confidence += 0.10

        # Macro confirmation
        if macro_bullish or macro_bearish:
            confidence += 0.10

        # Breakout
        if breakout:
            confidence += 0.10

        # Momentum confirmation
        if (
            trend == "BULLISH"
            and momentum == "POSITIVE"
        ):
            confidence += 0.05

        elif (
            trend == "BEARISH"
            and momentum == "NEGATIVE"
        ):
            confidence += 0.05

        # Volatility expansion is meaningful,
        # but should not automatically imply certainty.
        if volatility == "EXPANDING":
            confidence += 0.05

        # Range environments require slightly less
        # confidence because they are inherently less directional.
        if regime == "RANGE":
            confidence -= 0.05

        return round(
            max(
                0.0,
                min(
                    confidence,
                    0.95,
                ),
            ),
            2,
        )

    # ------------------------------------------------------------------
    # REGIME ACCEPTANCE
    # ------------------------------------------------------------------

    def _regime_allowed(
        self,
        regime: str,
        confidence: float,
        adx: float,
        breakout: bool,
        volatility: str,
        trend: str,
    ) -> tuple[bool, str]:

        if regime == "UNKNOWN":
            return False, "UNKNOWN_REGIME"

        if confidence < 0.40:
            return False, "LOW_CONFIDENCE"

        # Volatility regimes are allowed when there is evidence
        # of expansion, elevated volatility or a breakout.
        if regime == "VOLATILITY":

            if (
                volatility in {
                    "EXPANDING",
                    "HIGH",
                }
                or breakout
            ):
                return True, "REGIME_ACCEPTED"

            return False, "WEAK_VOLATILITY_SIGNAL"

        # Directional regimes should have at least some trend evidence.
        if regime in {
            "BULLISH",
            "BEARISH",
        }:

            if (
                adx >= 20
                or breakout
                or trend in {
                    "BULLISH",
                    "BEARISH",
                }
            ):
                return True, "REGIME_ACCEPTED"

            return False, "WEAK_TREND"

        # Range is valid when there is no strong directional trend.
        if regime == "RANGE":

            if adx < 25:
                return True, "REGIME_ACCEPTED"

            return False, "STRONG_TREND_CONFLICT"

        return False, "UNKNOWN_REGIME"

    # ------------------------------------------------------------------
    # UNKNOWN RESULT
    # ------------------------------------------------------------------

    @staticmethod
    def _unknown_result(
        reason: str = "UNKNOWN",
    ) -> Dict[str, Any]:

        return {
            "trend": "UNKNOWN",
            "volatility": "UNKNOWN",
            "momentum": "UNKNOWN",
            "regime": "UNKNOWN",
            "environment": "UNKNOWN",
            "confidence": 0.0,
            "allowed": False,
            "reason": reason,
            "atr_ratio": 0.0,
            "adx": 0.0,
            "ema_gap": 0.0,
            "breakout": False,
            "breakout_up": False,
            "breakout_down": False,
            "bollinger_expanding": False,
            "bullish_structure": False,
            "bearish_structure": False,
            "strong_trend": False,
            "macro_bullish": False,
            "macro_bearish": False,
        }