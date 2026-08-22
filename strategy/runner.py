"""
Atlas AI Trading Platform 4.4

Adaptive Strategy Runner

Central single-candle decision engine.

Pipeline:

    Market Data
        |
        v
    Regime Detector
        |
        v
    Regime Filter
        |
        +---- BLOCKED ----> No Signal
        |
        v
    Strategy Router
        |
        v
    Active Strategy
        |
        v
    Normalised Signal
        |
        v
    Strategy Score Floor
        |
        v
    Strategy Confidence Floor
        |
        v
    Final Signal

Used by:

- Backtesting
- Optimisation
- Validation
- Research

Important:

This class analyses ONE historical window at a time.

It does not advance through historical candles itself.
"""

from __future__ import annotations

import pandas as pd

from strategy.config import StrategyConfig
from strategy.router import StrategyRouter
from research.regime_detector import RegimeDetector


class StrategyRunner:

    def __init__(
        self,
        score_threshold=None,
        confidence_threshold=None,
    ):

        # -----------------------------------------------------
        # Optional external thresholds.
        #
        # These are allowed to make the strategy stricter,
        # but StrategyConfig always provides the minimum floor.
        # -----------------------------------------------------

        self.requested_score_threshold = (
            score_threshold
        )

        self.requested_confidence_threshold = (
            confidence_threshold
        )

        self.router = StrategyRouter()

        self.regime_detector = RegimeDetector()

        # -----------------------------------------------------
        # Diagnostics
        # -----------------------------------------------------

        self.total_windows = 0

        self.regime_blocked = 0

        self.regime_confidence_blocked = 0

        self.strategy_attempts = 0

        self.signals_generated = 0

        self.signals_rejected_score = 0

        self.signals_rejected_confidence = 0

        self.signals_rejected_direction = 0

        self.regime_counts = {

            "TREND":
                0,

            "BULLISH":
                0,

            "BEARISH":
                0,

            "RANGE":
                0,

            "SIDEWAYS":
                0,

            "VOLATILITY":
                0,

            "BREAKOUT":
                0,

            "UNKNOWN":
                0,

        }

    # =========================================================
    # STRATEGY NAME
    # =========================================================

    @staticmethod
    def _strategy_name(
        strategy,
        supplied_name=None,
    ):

        if isinstance(
            supplied_name,
            str,
        ):

            name = (
                supplied_name
                .strip()
            )

            if name and (
                name.upper()
                != "UNKNOWN"
            ):

                return name

        if strategy is not None:

            try:

                name = (
                    strategy.__class__.__name__
                )

                if name:

                    return name

            except Exception:

                pass

        return "UNKNOWN"

    # =========================================================
    # ANALYSE CURRENT WINDOW
    # =========================================================

    def analyse(
        self,
        dataframe: pd.DataFrame,
        strategy=None,
        symbol=None,
    ):

        self.total_windows += 1

        # =====================================================
        # BASIC VALIDATION
        # =====================================================

        if (
            dataframe is None
            or not isinstance(
                dataframe,
                pd.DataFrame,
            )
            or len(dataframe) < 50
        ):

            self.regime_blocked += 1

            self.regime_counts[
                "UNKNOWN"
            ] += 1

            return None

        # =====================================================
        # REGIME DETECTION
        # =====================================================

        regime_data = None

        if strategy is None:

            try:

                regime_data = (
                    self.regime_detector.analyse(
                        dataframe
                    )
                )

            except Exception:

                self.regime_blocked += 1

                self.regime_counts[
                    "UNKNOWN"
                ] += 1

                return None

            if not isinstance(
                regime_data,
                dict,
            ):

                self.regime_blocked += 1

                self.regime_counts[
                    "UNKNOWN"
                ] += 1

                return None

            regime_name = str(
                regime_data.get(
                    "regime",
                    "UNKNOWN",
                )
            ).upper().strip()

            allowed = bool(
                regime_data.get(
                    "allowed",
                    False,
                )
            )

            reason = regime_data.get(
                "reason",
                "UNKNOWN",
            )

        else:

            # -------------------------------------------------
            # Explicit strategy mode.
            #
            # Used only by callers intentionally supplying a
            # strategy directly.
            # -------------------------------------------------

            regime_name = "UNKNOWN"

            allowed = True

            reason = "EXPLICIT_STRATEGY"

            try:

                regime_data = (
                    self.regime_detector.analyse(
                        dataframe
                    )
                )

                if isinstance(
                    regime_data,
                    dict,
                ):

                    detected_regime = (
                        regime_data.get(
                            "regime"
                        )
                    )

                    if detected_regime:

                        regime_name = str(
                            detected_regime
                        ).upper().strip()

            except Exception:

                pass

        # =====================================================
        # RECORD REGIME
        # =====================================================

        if regime_name not in self.regime_counts:

            self.regime_counts[
                "UNKNOWN"
            ] += 1

        else:

            self.regime_counts[
                regime_name
            ] += 1

        # =====================================================
        # REGIME ALLOW/DENY FILTER
        # =====================================================

        if not allowed:

            self.regime_blocked += 1

            return None

        # =====================================================
        # REGIME CONFIDENCE FILTER
        #
        # Explicit strategy mode bypasses this because the
        # caller has deliberately selected the strategy.
        # =====================================================

        regime_confidence = 0.0

        if isinstance(
            regime_data,
            dict,
        ):

            try:

                regime_confidence = float(
                    regime_data.get(
                        "confidence",
                        0.0,
                    )
                )

            except (
                TypeError,
                ValueError,
            ):

                regime_confidence = 0.0

        if strategy is None:

            if regime_confidence < (
                StrategyConfig.MIN_REGIME_CONFIDENCE
            ):

                self.regime_confidence_blocked += 1

                return None

        # =====================================================
        # SELECT STRATEGY
        # =====================================================

        if strategy is None:

            try:

                strategy = self.router.select(
                    regime_name
                )

            except Exception:

                strategy = None

        # =====================================================
        # NO STRATEGY
        # =====================================================

        if strategy is None:

            self.regime_blocked += 1

            return None

        # =====================================================
        # LEGACY STRING PROTECTION
        # =====================================================

        if isinstance(
            strategy,
            str,
        ):

            if symbol is None:

                symbol = strategy

            strategy = None

            try:

                strategy = self.router.select(
                    regime_name
                )

            except Exception:

                return None

        if strategy is None:

            return None

        self.strategy_attempts += 1

        # =====================================================
        # STRATEGY NAME
        # =====================================================

        selected_strategy_name = (
            self._strategy_name(
                strategy
            )
        )

        # =====================================================
        # STRATEGY-SPECIFIC THRESHOLDS
        # =====================================================

        effective_score_threshold = (
            StrategyConfig.effective_score_threshold(
                selected_strategy_name,
                self.requested_score_threshold,
            )
        )

        effective_confidence_threshold = (
            StrategyConfig.effective_confidence_threshold(
                selected_strategy_name,
                self.requested_confidence_threshold,
            )
        )

        # =====================================================
        # GENERATE SIGNAL
        # =====================================================

        try:

            if hasattr(
                strategy,
                "generate_signal",
            ):

                signal = (
                    strategy.generate_signal(
                        dataframe
                    )
                )

            elif hasattr(
                strategy,
                "generate",
            ):

                signal = (
                    strategy.generate(
                        dataframe
                    )
                )

            else:

                return None

        except Exception:

            return None

        # =====================================================
        # NO SIGNAL
        # =====================================================

        if signal is None:

            return None

        # =====================================================
        # NORMALISE SIGNAL
        # =====================================================

        if isinstance(
            signal,
            dict,
        ):

            normalised = dict(
                signal
            )

        else:

            normalised = {

                "signal":
                    getattr(
                        signal,
                        "signal",
                        None,
                    ),

                "score":
                    getattr(
                        signal,
                        "score",
                        0,
                    ),

                "confidence":
                    getattr(
                        signal,
                        "confidence",
                        0,
                    ),

                "strategy":
                    getattr(
                        signal,
                        "strategy",
                        None,
                    ),

            }

        # =====================================================
        # CORE FIELDS
        # =====================================================

        bias = normalised.get(
            "signal"
        )

        score = normalised.get(
            "score",
            0,
        )

        confidence = normalised.get(
            "confidence",
            0,
        )

        # =====================================================
        # NUMERIC SAFETY
        # =====================================================

        try:

            score = float(
                score
            )

        except (
            TypeError,
            ValueError,
        ):

            score = 0.0

        try:

            confidence = float(
                confidence
            )

        except (
            TypeError,
            ValueError,
        ):

            confidence = 0.0

        # =====================================================
        # NORMALISE DIRECTION
        # =====================================================

        if isinstance(
            bias,
            str,
        ):

            bias = (
                bias
                .upper()
                .strip()
            )

        # =====================================================
        # DIRECTION FILTER
        # =====================================================

        if bias not in (
            "BUY",
            "SELL",
        ):

            self.signals_rejected_direction += 1

            return None

        # =====================================================
        # SCORE FILTER
        # =====================================================

        if abs(
            score
        ) < effective_score_threshold:

            self.signals_rejected_score += 1

            return None

        # =====================================================
        # CONFIDENCE FILTER
        # =====================================================

        if confidence < (
            effective_confidence_threshold
        ):

            self.signals_rejected_confidence += 1

            return None

        # =====================================================
        # SUCCESS
        # =====================================================

        self.signals_generated += 1

        # =====================================================
        # STRATEGY ATTRIBUTION
        # =====================================================

        strategy_name = (
            self._strategy_name(
                strategy,
                normalised.get(
                    "strategy"
                ),
            )
        )

        # =====================================================
        # RESULT
        # =====================================================

        result = {

            "signal":
                bias,

            "bias":
                bias,

            "score":
                score,

            "confidence":
                confidence,

            "strategy":
                strategy_name,

            "selected_strategy":
                strategy_name,

            "regime":
                regime_name,

            "regime_allowed":
                allowed,

            "regime_reason":
                reason,

            "score_threshold":
                effective_score_threshold,

            "confidence_threshold":
                effective_confidence_threshold,

            "regime_confidence":
                regime_confidence,

        }

        # =====================================================
        # PRESERVE REGIME DIAGNOSTICS
        # =====================================================

        if isinstance(
            regime_data,
            dict,
        ):

            for key in (

                "trend",
                "volatility",
                "momentum",
                "adx",
                "atr_ratio",
                "ema_gap",
                "breakout",
                "breakout_up",
                "breakout_down",
                "bollinger_expanding",
                "bullish_structure",
                "bearish_structure",
                "strong_trend",
                "macro_bullish",
                "macro_bearish",

            ):

                if key in regime_data:

                    result[key] = (
                        regime_data[key]
                    )

        # =====================================================
        # PRESERVE STRATEGY METADATA
        # =====================================================

        for key in (

            "reason",
            "strength",
            "direction",

        ):

            if key in normalised:

                result[key] = (
                    normalised[key]
                )

        # =====================================================
        # SYMBOL
        # =====================================================

        if symbol is not None:

            result["symbol"] = symbol

        return result

    # =========================================================
    # RUN
    # =========================================================

    def run(
        self,
        dataframe: pd.DataFrame = None,
        strategy=None,
        symbol=None,
        **kwargs,
    ):

        if dataframe is None:

            dataframe = kwargs.get(
                "data"
            )

        if symbol is None:

            symbol = kwargs.get(
                "symbol"
            )

        if isinstance(
            strategy,
            str,
        ):

            if symbol is None:

                symbol = strategy

            strategy = None

        return self.analyse(
            dataframe=dataframe,
            strategy=strategy,
            symbol=symbol,
        )

    # =========================================================
    # DIAGNOSTICS
    # =========================================================

    def statistics(self) -> dict:

        return {

            "total_windows":
                self.total_windows,

            "regime_blocked":
                self.regime_blocked,

            "regime_confidence_blocked":
                self.regime_confidence_blocked,

            "strategy_attempts":
                self.strategy_attempts,

            "signals_generated":
                self.signals_generated,

            "signals_rejected_direction":
                self.signals_rejected_direction,

            "signals_rejected_score":
                self.signals_rejected_score,

            "signals_rejected_confidence":
                self.signals_rejected_confidence,

            "regimes":
                self.regime_counts.copy(),

        }