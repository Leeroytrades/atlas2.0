"""
Atlas AI Trading Platform 4.0

Validation Metrics

Used for:

- Walk forward validation
- Robustness scoring
- Strategy acceptance
- Overfit protection
- Statistical confidence classification

Validation philosophy:

A validation window can perform well while containing only a
small number of trades.

Therefore:

    PERFORMANCE
        and
    SAMPLE SIZE

are treated as separate concepts.

A window can therefore be classified as:

    PASS
        Strong performance + sufficient sample.

    PASS_LOW_SAMPLE
        Strong performance + insufficient sample.

    FAIL
        Performance or robustness requirements not satisfied.

This prevents a good but low-frequency strategy from being
incorrectly labelled as a normal failure while still making
the statistical limitation explicit.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ValidationMetrics:

    profit: float = 0.0

    win_rate: float = 0.0

    profit_factor: float = 0.0

    total_trades: int = 0

    winning_trades: int = 0

    losing_trades: int = 0

    max_drawdown: float = 0.0

    stability_score: float = 0.0

    # =====================================================
    # CONFIGURATION
    # =====================================================

    # Minimum number of trades required before a validation
    # result can be considered statistically sufficient.
    #
    # This does NOT automatically cause a performance failure.
    MIN_SAMPLE_SIZE = 10

    # Minimum acceptable profit factor.
    MIN_PROFIT_FACTOR = 1.30

    # Maximum acceptable drawdown percentage.
    MAX_DRAWDOWN = 25.0

    # Minimum robustness score required for performance pass.
    MIN_ROBUSTNESS_SCORE = 70.0

    # =====================================================
    # BUILD FROM BACKTEST RESULT
    # =====================================================

    @classmethod
    def from_result(
        cls,
        result: dict,
    ):

        if not isinstance(result, dict):

            result = {}

        trades = result.get(
            "trade_list",
            result.get(
                "trades",
                []
            )
        )

        winning = 0

        losing = 0

        gross_profit = 0.0

        gross_loss = 0.0

        # -------------------------------------------------
        # Calculate directly from trade list
        # -------------------------------------------------

        if isinstance(trades, list):

            for trade in trades:

                if isinstance(trade, dict):

                    pnl = trade.get(
                        "profit_loss",
                        trade.get(
                            "pnl",
                            0
                        )
                    )

                else:

                    pnl = getattr(
                        trade,
                        "profit_loss",
                        getattr(
                            trade,
                            "pnl",
                            0
                        )
                    )

                try:

                    pnl = float(pnl)

                except (
                    TypeError,
                    ValueError,
                ):

                    pnl = 0.0

                if pnl > 0:

                    winning += 1

                    gross_profit += pnl

                elif pnl < 0:

                    losing += 1

                    gross_loss += abs(pnl)

            total = winning + losing

            if total > 0:

                win_rate = (
                    winning
                    / total
                    * 100
                )

            else:

                win_rate = 0.0

            if gross_loss > 0:

                profit_factor = (
                    gross_profit
                    / gross_loss
                )

            elif gross_profit > 0:

                # There are profits but no observed losses.
                #
                # Raw PF is mathematically infinite, but we
                # cap it for validation/scoring purposes.
                profit_factor = 10.0

            else:

                profit_factor = 0.0

        # -------------------------------------------------
        # Fallback when no trade list exists
        # -------------------------------------------------

        else:

            total = result.get(
                "total_trades",
                result.get(
                    "trades",
                    0
                )
            )

            winning = result.get(
                "winning_trades",
                result.get(
                    "wins",
                    0
                )
            )

            losing = result.get(
                "losing_trades",
                result.get(
                    "losses",
                    0
                )
            )

            win_rate = result.get(
                "win_rate",
                0
            )

            profit_factor = result.get(
                "profit_factor",
                0
            )

        # -------------------------------------------------
        # Profit
        # -------------------------------------------------

        try:

            profit = float(
                result.get(
                    "profit",
                    result.get(
                        "net_profit",
                        0
                    )
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            profit = 0.0

        # -------------------------------------------------
        # Drawdown
        # -------------------------------------------------

        try:

            max_drawdown = float(
                result.get(
                    "max_drawdown",
                    0
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            max_drawdown = 0.0

        # -------------------------------------------------
        # Stability
        # -------------------------------------------------

        try:

            stability_score = float(
                result.get(
                    "stability_score",
                    0
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            stability_score = 0.0

        # -------------------------------------------------
        # Safe numeric conversion
        # -------------------------------------------------

        try:

            total = int(total)

        except (
            TypeError,
            ValueError,
        ):

            total = 0

        try:

            winning = int(winning)

        except (
            TypeError,
            ValueError,
        ):

            winning = 0

        try:

            losing = int(losing)

        except (
            TypeError,
            ValueError,
        ):

            losing = 0

        try:

            win_rate = float(
                win_rate
            )

        except (
            TypeError,
            ValueError,
        ):

            win_rate = 0.0

        try:

            profit_factor = float(
                profit_factor
            )

        except (
            TypeError,
            ValueError,
        ):

            profit_factor = 0.0

        return cls(

            profit=profit,

            win_rate=win_rate,

            profit_factor=profit_factor,

            total_trades=total,

            winning_trades=winning,

            losing_trades=losing,

            max_drawdown=max_drawdown,

            stability_score=stability_score,

        )

    # =====================================================
    # PERFORMANCE PASS
    # =====================================================

    def performance_passes(
        self,
    ):
        """
        Determines whether the validation window satisfies
        the actual trading-performance requirements.

        Trade count is deliberately NOT checked here.

        This allows us to distinguish:

            Good performance + low sample

        from:

            Bad performance.
        """

        if self.profit <= 0:

            return False

        if self.profit_factor < self.MIN_PROFIT_FACTOR:

            return False

        if self.max_drawdown > self.MAX_DRAWDOWN:

            return False

        if self.robustness_score() < self.MIN_ROBUSTNESS_SCORE:

            return False

        return True

    # =====================================================
    # ROBUSTNESS SCORE
    # =====================================================

    def robustness_score(
        self,
    ):
        """
        Calculate a 0-100 robustness score.

        The score deliberately caps the contribution of
        extreme profit factors.

        This is important because a result such as:

            7 trades
            PF 698

        should NOT receive dramatically more credit than:

            7 trades
            PF 3.

        The raw PF is retained for reporting, but only a
        capped PF contributes to robustness scoring.
        """

        score = 0.0

        # -------------------------------------------------
        # PROFIT
        # -------------------------------------------------

        if self.profit > 0:

            score += 25

        # -------------------------------------------------
        # TRADE SAMPLE
        #
        # Sample size contributes to robustness but does
        # not independently cause a performance failure.
        # -------------------------------------------------

        if self.total_trades >= 30:

            score += 15

        elif self.total_trades >= 20:

            score += 12

        elif self.total_trades >= 10:

            score += 8

        elif self.total_trades >= 5:

            score += 4

        else:

            score += 0

        # -------------------------------------------------
        # PROFIT FACTOR
        #
        # Cap PF at 4 for scoring.
        # -------------------------------------------------

        pf = min(
            max(
                self.profit_factor,
                0.0
            ),
            4.0
        )

        if pf >= 3:

            score += 25

        elif pf >= 2:

            score += 20

        elif pf >= 1.5:

            score += 15

        elif pf >= 1.3:

            score += 10

        elif pf >= 1:

            score += 5

        # -------------------------------------------------
        # DRAWDOWN
        # -------------------------------------------------

        if self.max_drawdown <= 5:

            score += 20

        elif self.max_drawdown <= 10:

            score += 15

        elif self.max_drawdown <= 15:

            score += 10

        elif self.max_drawdown <= 25:

            score += 0

        else:

            score -= 40

        # -------------------------------------------------
        # STABILITY
        # -------------------------------------------------

        if self.stability_score >= 80:

            score += 15

        elif self.stability_score >= 60:

            score += 10

        elif self.stability_score >= 40:

            score += 5

        return max(
            0,
            min(
                round(
                    score,
                    2
                ),
                100
            )
        )

    # =====================================================
    # SAMPLE SUFFICIENCY
    # =====================================================

    def sample_is_sufficient(
        self,
    ):
        """
        Determine whether the validation window contains
        enough trades to provide a reasonably useful sample.

        This is a statistical-confidence test.

        It is NOT a performance test.
        """

        return (
            self.total_trades
            >= self.MIN_SAMPLE_SIZE
        )

    # =====================================================
    # PASS / FAIL
    # =====================================================

    def passes(
        self,
    ):
        """
        Backwards-compatible performance PASS method.

        Returns True when the actual trading-performance
        requirements are satisfied.

        It intentionally does NOT require 10+ trades.

        Use classification() when the distinction between
        PASS and PASS_LOW_SAMPLE is required.
        """

        return self.performance_passes()

    # =====================================================
    # CLASSIFICATION
    # =====================================================

    def classification(
        self,
    ):
        """
        Return the final validation classification.

        PASS
            Performance passes and sample is sufficient.

        PASS_LOW_SAMPLE
            Performance passes but sample size is too small
            to provide strong statistical confidence.

        FAIL
            Performance requirements are not satisfied.
        """

        if not self.performance_passes():

            return "FAIL"

        if not self.sample_is_sufficient():

            return "PASS_LOW_SAMPLE"

        return "PASS"

    # =====================================================
    # FAILURE REASONS
    # =====================================================

    def failure_reasons(
        self,
    ):
        """
        Return diagnostic reasons.

        INSUFFICIENT_SAMPLE is intentionally NOT considered
        an actual performance failure.

        It is a statistical-confidence warning.
        """

        reasons = []

        if self.profit <= 0:

            reasons.append(
                "NON_POSITIVE_PROFIT"
            )

        if self.profit_factor < self.MIN_PROFIT_FACTOR:

            reasons.append(
                "LOW_PROFIT_FACTOR"
            )

        if self.max_drawdown > self.MAX_DRAWDOWN:

            reasons.append(
                "EXCESSIVE_DRAWDOWN"
            )

        if not self.sample_is_sufficient():

            reasons.append(
                "INSUFFICIENT_SAMPLE"
            )

        if self.robustness_score() < self.MIN_ROBUSTNESS_SCORE:

            reasons.append(
                "LOW_ROBUSTNESS_SCORE"
            )

        return reasons

    # =====================================================
    # PERFORMANCE FAILURE REASONS
    # =====================================================

    def performance_failure_reasons(
        self,
    ):
        """
        Return only genuine performance/robustness failures.

        This deliberately excludes INSUFFICIENT_SAMPLE.
        """

        reasons = []

        if self.profit <= 0:

            reasons.append(
                "NON_POSITIVE_PROFIT"
            )

        if self.profit_factor < self.MIN_PROFIT_FACTOR:

            reasons.append(
                "LOW_PROFIT_FACTOR"
            )

        if self.max_drawdown > self.MAX_DRAWDOWN:

            reasons.append(
                "EXCESSIVE_DRAWDOWN"
            )

        if self.robustness_score() < self.MIN_ROBUSTNESS_SCORE:

            reasons.append(
                "LOW_ROBUSTNESS_SCORE"
            )

        return reasons

    # =====================================================
    # OUTPUT
    # =====================================================

    def to_dict(
        self,
    ):

        return {

            "profit":
                round(
                    self.profit,
                    2
                ),

            "win_rate":
                round(
                    self.win_rate,
                    2
                ),

            "profit_factor":
                round(
                    self.profit_factor,
                    2
                ),

            "total_trades":
                self.total_trades,

            "winning_trades":
                self.winning_trades,

            "losing_trades":
                self.losing_trades,

            "max_drawdown":
                round(
                    self.max_drawdown,
                    2
                ),

            "stability_score":
                round(
                    self.stability_score,
                    2
                ),

            "robustness_score":
                self.robustness_score(),

            "sample_sufficient":
                self.sample_is_sufficient(),

            "classification":
                self.classification(),

            "failure_reasons":
                self.failure_reasons(),

            "performance_failure_reasons":
                self.performance_failure_reasons(),

        }