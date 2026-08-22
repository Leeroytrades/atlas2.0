"""
Atlas AI Trading Platform 4.3

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
    Score Filter
        |
        v
    Confidence Filter
        |
        v
    Final Signal

Used by:

- Backtesting
- Optimisation
- Validation
- Research
"""

from __future__ import annotations

import pandas as pd

from strategy.router import StrategyRouter
from research.regime_detector import RegimeDetector


class StrategyRunner:

    def __init__(
        self,
        score_threshold: int = 40,
        confidence_threshold: float = 0.40,
    ):

        self.score_threshold = float(
            score_threshold
        )

        self.confidence_threshold = float(
            confidence_threshold
        )

        self.router = StrategyRouter()

        self.regime_detector = RegimeDetector()

        # -------------------------------------------------
        # Diagnostics
        # -------------------------------------------------

        self.total_windows = 0
        self.regime_blocked = 0
        self.strategy_attempts = 0
        self.signals_generated = 0
        self.signals_rejected_score = 0
        self.signals_rejected_confidence = 0

        self.regime_counts = {
            "BULLISH": 0,
            "BEARISH": 0,
            "RANGE": 0,
            "VOLATILITY": 0,
            "UNKNOWN": 0,
        }

    # =====================================================
    # STRATEGY NAME
    # =====================================================

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

    # =====================================================
    # ANALYSE CURRENT WINDOW
    # =====================================================

    def analyse(
        self,
        dataframe: pd.DataFrame,
        strategy=None,
        symbol=None,
    ):

        self.total_windows += 1

        # -------------------------------------------------
        # Basic validation
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Determine regime
        # -------------------------------------------------

        regime_data = None

        if strategy is None:

            try:

                regime_data = (
                    self.regime_detector.analyse(
                        dataframe
                    )
                )

            except Exception as exc:

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
            # This preserves compatibility for callers that
            # intentionally supply a strategy directly.
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

        # -------------------------------------------------
        # Record regime statistics
        # -------------------------------------------------

        if regime_name not in self.regime_counts:

            self.regime_counts[
                "UNKNOWN"
            ] += 1

        else:

            self.regime_counts[
                regime_name
            ] += 1

        # -------------------------------------------------
        # REGIME FILTER
        #
        # This is the critical gate.
        #
        # UNKNOWN/RANGE/etc. cannot reach the strategy
        # unless the RegimeFilter explicitly allows them.
        # -------------------------------------------------

        if not allowed:

            self.regime_blocked += 1

            return None

        # -------------------------------------------------
        # Select strategy
        # -------------------------------------------------

        if strategy is None:

            try:

                strategy = self.router.select(
                    regime_name
                )

            except Exception:

                strategy = None

        # -------------------------------------------------
        # No strategy
        # -------------------------------------------------

        if strategy is None:

            self.regime_blocked += 1

            return None

        # -------------------------------------------------
        # Legacy protection
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Determine selected strategy
        # -------------------------------------------------

        selected_strategy_name = (
            self._strategy_name(
                strategy
            )
        )

        # -------------------------------------------------
        # Generate signal
        # -------------------------------------------------

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

        # -------------------------------------------------
        # No signal
        # -------------------------------------------------

        if signal is None:

            return None

        # -------------------------------------------------
        # Normalise object / dict
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Core fields
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Numeric safety
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Signal normalisation
        # -------------------------------------------------

        if isinstance(
            bias,
            str,
        ):

            bias = (
                bias
                .upper()
                .strip()
            )

        # -------------------------------------------------
        # Direction check
        # -------------------------------------------------

        if bias not in (
            "BUY",
            "SELL",
        ):

            return None

        # -------------------------------------------------
        # Score filter
        # -------------------------------------------------

        if abs(
            score
        ) < self.score_threshold:

            self.signals_rejected_score += 1

            return None

        # -------------------------------------------------
        # Confidence filter
        # -------------------------------------------------

        if confidence < (
            self.confidence_threshold
        ):

            self.signals_rejected_confidence += 1

            return None

        # -------------------------------------------------
        # Successful signal
        # -------------------------------------------------

        self.signals_generated += 1

        # -------------------------------------------------
        # Strategy attribution
        # -------------------------------------------------

        strategy_name = (
            self._strategy_name(
                strategy,
                normalised.get(
                    "strategy"
                ),
            )
        )

        # -------------------------------------------------
        # Build result
        # -------------------------------------------------

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

        }

        # -------------------------------------------------
        # Preserve detector diagnostics
        # -------------------------------------------------

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

            if "confidence" in regime_data:

                result[
                    "regime_confidence"
                ] = regime_data[
                    "confidence"
                ]

        # -------------------------------------------------
        # Preserve strategy metadata
        # -------------------------------------------------

        for key in (
            "reason",
            "strength",
            "direction",
        ):

            if key in normalised:

                result[key] = (
                    normalised[key]
                )

        # -------------------------------------------------
        # Symbol
        # -------------------------------------------------

        if symbol is not None:

            result["symbol"] = symbol

        return result

    # =====================================================
    # RUN
    # =====================================================

    def run(
        self,
        dataframe: pd.DataFrame = None,
        strategy=None,
        symbol=None,
        **kwargs,
    ):

        # -------------------------------------------------
        # Recover dataframe
        # -------------------------------------------------

        if dataframe is None:

            dataframe = kwargs.get(
                "data"
            )

        # -------------------------------------------------
        # Recover symbol
        # -------------------------------------------------

        if symbol is None:

            symbol = kwargs.get(
                "symbol"
            )

        # -------------------------------------------------
        # Legacy protection
        # -------------------------------------------------

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

    # =====================================================
    # DIAGNOSTICS
    # =====================================================

    def statistics(self) -> dict:

        return {

            "total_windows":
                self.total_windows,

            "regime_blocked":
                self.regime_blocked,

            "strategy_attempts":
                self.strategy_attempts,

            "signals_generated":
                self.signals_generated,

            "signals_rejected_score":
                self.signals_rejected_score,

            "signals_rejected_confidence":
                self.signals_rejected_confidence,

            "regimes":
                self.regime_counts.copy(),

        }