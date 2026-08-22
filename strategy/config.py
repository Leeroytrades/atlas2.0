"""
Atlas AI Trading Platform 4.4

Strategy Configuration

Central source of truth for:

- Strategy score floors
- Strategy confidence floors
- Minimum regime confidence
- Signal quality controls
- Execution spacing controls

Design rule:

Strategy-specific thresholds are minimum quality floors.

A caller such as the optimiser may request a stricter
threshold, but it cannot lower the configured strategy floor.
"""

from __future__ import annotations


class StrategyConfig:

    # =========================================================
    # STRATEGY SCORE FLOORS
    # =========================================================

    SCORE_THRESHOLDS = {

        "TrendStrategy":
            50,

        "RangeStrategy":
            45,

        "VolatilityStrategy":
            60,

    }

    # =========================================================
    # STRATEGY CONFIDENCE FLOORS
    # =========================================================

    CONFIDENCE_THRESHOLDS = {

        "TrendStrategy":
            0.55,

        "RangeStrategy":
            0.60,

        "VolatilityStrategy":
            0.65,

    }

    # =========================================================
    # REGIME CONFIDENCE
    # =========================================================

    MIN_REGIME_CONFIDENCE = 0.70

    # =========================================================
    # SIGNAL QUALITY
    #
    # Reserved for a future explicit score-separation rule.
    #
    # It is deliberately NOT applied automatically because
    # "score distance" has not yet been formally defined.
    # =========================================================

    MIN_SCORE_DISTANCE = 10

    # =========================================================
    # TRADE SPACING
    #
    # Minimum number of candles between the previous trade exit
    # and the next eligible signal candle.
    # =========================================================

    MIN_CANDLES_BETWEEN_TRADES = 20

    # =========================================================
    # THRESHOLD HELPERS
    # =========================================================

    @classmethod
    def score_threshold(
        cls,
        strategy,
    ) -> float:

        return float(
            cls.SCORE_THRESHOLDS.get(
                strategy,
                50,
            )
        )

    @classmethod
    def confidence_threshold(
        cls,
        strategy,
    ) -> float:

        return float(
            cls.CONFIDENCE_THRESHOLDS.get(
                strategy,
                0.50,
            )
        )

    # =========================================================
    # EFFECTIVE THRESHOLDS
    # =========================================================

    @classmethod
    def effective_score_threshold(
        cls,
        strategy,
        requested=None,
    ) -> float:
        """
        Return the actual score threshold.

        The strategy configuration is always the minimum floor.

        If a caller supplies a higher threshold, the higher
        threshold is used.

        Example:

            Strategy floor = 50
            Requested      = 40
            Effective      = 50

            Strategy floor = 50
            Requested      = 70
            Effective      = 70
        """

        floor = cls.score_threshold(
            strategy
        )

        if requested is None:

            return floor

        try:

            requested = float(
                requested
            )

        except (
            TypeError,
            ValueError,
        ):

            return floor

        return max(
            floor,
            requested,
        )

    @classmethod
    def effective_confidence_threshold(
        cls,
        strategy,
        requested=None,
    ) -> float:
        """
        Return the actual confidence threshold.

        The strategy configuration is always the minimum floor.
        """

        floor = cls.confidence_threshold(
            strategy
        )

        if requested is None:

            return floor

        try:

            requested = float(
                requested
            )

        except (
            TypeError,
            ValueError,
        ):

            return floor

        return max(
            floor,
            requested,
        )