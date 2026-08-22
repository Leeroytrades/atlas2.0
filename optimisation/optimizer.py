"""
Atlas AI Trading Platform 4.2

Strategy Optimiser

Searches parameter combinations and ranks them using:

- Profit
- Profit Factor
- Drawdown
- Trade count
- Win rate
- Average trade
- Stability protection

The optimiser is deliberately conservative.

A configuration that produces a large profit from
very few trades should not automatically win the
optimisation simply because of a high profit factor.

Atlas 4.2 improvements:

- Zero-trade configurations cannot win optimisation.
- Invalid / non-trading configurations are explicitly marked.
- Best configuration selection ignores invalid results.
- Training optimisation diagnostics are preserved.
"""

from __future__ import annotations

from itertools import product

from optimisation.parallel_runner import ParallelOptimizer


class StrategyOptimizer:

    # =====================================================
    # CONSTANTS
    # =====================================================

    INVALID_SCORE = -1_000_000.0

    MINIMUM_VALID_TRADES = 1

    # =====================================================
    # INIT
    # =====================================================

    def __init__(
        self,
        starting_cash: float = 100000.0,
    ):

        self.starting_cash = float(
            starting_cash
        )

        self.parallel_runner = (
            ParallelOptimizer()
        )

    # =====================================================
    # GENERATE CONFIGURATIONS
    # =====================================================

    def generate_configurations(
        self,
        scores=None,
        confidences=None,
        atr_stops=None,
        atr_targets=None,
    ):

        scores = scores or [
            40,
            50,
            60,
            70,
            80,
        ]

        confidences = confidences or [
            0.4,
            0.5,
            0.6,
        ]

        atr_stops = atr_stops or [
            2.5,
            3.0,
        ]

        atr_targets = atr_targets or [
            4.0,
            5.0,
            5.5,
            6.0,
        ]

        configurations = []

        for (
            score,
            confidence,
            atr_stop,
            atr_target,
        ) in product(
            scores,
            confidences,
            atr_stops,
            atr_targets,
        ):

            configurations.append(
                {
                    "score_threshold": score,
                    "confidence": confidence,
                    "atr_stop": atr_stop,
                    "atr_target": atr_target,
                }
            )

        print()

        print(
            f"Generated "
            f"{len(configurations)} "
            f"optimisation configurations"
        )

        return configurations

    # =====================================================
    # EXTRACT TRADE COUNT
    # =====================================================

    @staticmethod
    def get_trade_count(
        result: dict,
    ) -> int:

        try:

            return int(
                result.get(
                    "total_trades",
                    result.get(
                        "trades",
                        0,
                    ),
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            return 0

    # =====================================================
    # VALIDATE RESULT
    # =====================================================

    def is_valid_result(
        self,
        result: dict,
    ) -> bool:
        """
        Determine whether an optimisation result actually
        contains enough information to be considered a
        trading configuration.

        A zero-trade configuration is never valid.

        This is deliberately separate from the statistical
        acceptance rules used during walk-forward validation.

        The optimiser only needs to know:

            "Did this configuration actually trade?"

        Validation later decides whether the resulting
        performance is statistically robust.
        """

        if not isinstance(
            result,
            dict,
        ):

            return False

        trades = self.get_trade_count(
            result
        )

        if trades < self.MINIMUM_VALID_TRADES:

            return False

        return True

    # =====================================================
    # SCORE RESULT
    # =====================================================

    def calculate_score(
        self,
        result: dict,
    ):
        """
        Calculate optimisation ranking score.

        Zero-trade configurations receive INVALID_SCORE
        and therefore cannot win optimisation.
        """

        if not self.is_valid_result(
            result
        ):

            return self.INVALID_SCORE

        # =================================================
        # PROFIT
        # =================================================

        try:

            profit = float(
                result.get(
                    "profit",
                    result.get(
                        "net_profit",
                        0,
                    ),
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            profit = 0.0

        # =================================================
        # PROFIT FACTOR
        # =================================================

        try:

            profit_factor = float(
                result.get(
                    "profit_factor",
                    0,
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            profit_factor = 0.0

        # =================================================
        # WIN RATE
        # =================================================

        try:

            win_rate = float(
                result.get(
                    "win_rate",
                    0,
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            win_rate = 0.0

        # =================================================
        # TRADE COUNT
        # =================================================

        trades = self.get_trade_count(
            result
        )

        # =================================================
        # DRAWDOWN
        # =================================================

        try:

            drawdown = float(
                result.get(
                    "max_drawdown",
                    0,
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            drawdown = 0.0

        # =================================================
        # AVERAGE TRADE
        # =================================================

        try:

            average_trade = float(
                result.get(
                    "average_trade",
                    0,
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            average_trade = 0.0

        # =================================================
        # START
        # =================================================

        score = 0.0

        # =================================================
        # PROFIT
        #
        # Profit matters, but should not dominate.
        # =================================================

        if self.starting_cash > 0:

            profit_percent = (
                profit
                /
                self.starting_cash
                *
                100
            )

        else:

            profit_percent = 0.0

        score += (
            profit_percent
            * 4
        )

        # =================================================
        # PROFIT FACTOR
        # =================================================

        if profit_factor >= 2.0:

            score += 30

        elif profit_factor >= 1.5:

            score += 20

        elif profit_factor >= 1.2:

            score += 12

        elif profit_factor >= 1.0:

            score += 5

        elif profit_factor > 0:

            score -= 25

        else:

            score -= 50

        # =================================================
        # DRAWDOWN
        # =================================================

        if drawdown <= 5:

            score += 30

        elif drawdown <= 10:

            score += 20

        elif drawdown <= 15:

            score += 5

        elif drawdown <= 20:

            score -= 10

        elif drawdown <= 30:

            score -= 40

        else:

            score -= 100

        # =================================================
        # TRADE COUNT
        #
        # A meaningful sample is rewarded.
        #
        # We do NOT require 30+ trades because selective
        # strategies can legitimately trade less frequently.
        # =================================================

        if trades >= 50:

            score += 15

        elif trades >= 30:

            score += 10

        elif trades >= 20:

            score += 5

        elif trades >= 10:

            score -= 5

        elif trades >= 5:

            score -= 20

        else:

            score -= 50

        # =================================================
        # WIN RATE
        # =================================================

        if win_rate >= 55:

            score += 15

        elif win_rate >= 45:

            score += 10

        elif win_rate >= 35:

            score += 5

        elif win_rate < 25:

            score -= 20

        # =================================================
        # AVERAGE TRADE
        # =================================================

        if average_trade > 0:

            score += 5

        elif average_trade < 0:

            score -= 10

        # =================================================
        # OVERFIT PROTECTION
        # =================================================

        if (
            trades < 10
            and profit_factor > 2
        ):

            score -= 30

        if (
            trades < 20
            and profit_factor > 4
        ):

            score -= 20

        # =================================================
        # LARGE PROFIT / SMALL SAMPLE PROTECTION
        # =================================================

        if (
            profit_percent > 15
            and trades < 20
        ):

            score -= 30

        # =================================================
        # EXTREME PROFIT FACTOR
        # =================================================

        if profit_factor > 10:

            score -= 50

        # =================================================
        # NEGATIVE PROFIT
        # =================================================

        if profit <= 0:

            score -= 30

        return round(
            score,
            2,
        )

    # =====================================================
    # OPTIMISE
    # =====================================================

    def optimise(
        self,
        dataset,
        symbol: str,
        configurations=None,
    ):

        if configurations is None:

            configurations = (
                self.generate_configurations()
            )

        print()

        print(
            f"Running "
            f"{len(configurations)} "
            f"optimisation tests"
        )

        results = (
            self.parallel_runner.run(
                dataset,
                symbol,
                self.starting_cash,
                configurations,
            )
        )

        if results is None:

            results = []

        # -------------------------------------------------
        # Calculate ranking scores
        # -------------------------------------------------

        valid_results = 0
        invalid_results = 0

        for result in results:

            if self.is_valid_result(
                result
            ):

                valid_results += 1

            else:

                invalid_results += 1

            result["ranking_score"] = (
                self.calculate_score(
                    result
                )
            )

            result["optimisation_valid"] = (
                self.is_valid_result(
                    result
                )
            )

        # -------------------------------------------------
        # Sort valid configurations first
        # -------------------------------------------------

        results.sort(
            key=lambda result:
                result.get(
                    "ranking_score",
                    self.INVALID_SCORE,
                ),
            reverse=True,
        )

        print()

        print(
            "OPTIMISATION SUMMARY"
        )

        print(
            f"Valid trading configurations: "
            f"{valid_results}"
        )

        print(
            f"Zero-trade / invalid configurations: "
            f"{invalid_results}"
        )

        # -------------------------------------------------
        # No usable configurations
        # -------------------------------------------------

        if valid_results == 0:

            print()

            print(
                "WARNING: NO VALID TRADING "
                "CONFIGURATION FOUND"
            )

            print(
                "Every optimisation configuration "
                "produced zero trades."
            )

        else:

            best_result = results[0]

            print()

            print(
                "BEST VALID CONFIGURATION"
            )

            print(
                f"Ranking score: "
                f"{best_result.get('ranking_score', 0):.2f}"
            )

            print(
                f"Training profit: "
                f"{best_result.get('profit', 0):.2f}"
            )

            print(
                f"Training trades: "
                f"{self.get_trade_count(best_result)}"
            )

            print(
                f"Training win rate: "
                f"{best_result.get('win_rate', 0):.2f}%"
            )

            print(
                f"Training profit factor: "
                f"{best_result.get('profit_factor', 0):.2f}"
            )

            print(
                f"Training max drawdown: "
                f"{best_result.get('max_drawdown', 0):.2f}%"
            )

        return results

    # =====================================================
    # BEST RESULT
    # =====================================================

    def best(
        self,
        results,
    ):

        if not results:

            return None

        for result in results:

            if self.is_valid_result(
                result
            ):

                return result

        return None