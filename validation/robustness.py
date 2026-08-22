
"""
Atlas AI Trading Platform 4.3

Validation Robustness Scoring Engine

Analyses completed walk-forward results.

IMPORTANT:
This module does NOT modify:
- Optimisation
- Backtesting
- Simulation
- Strategy logic
- Validation thresholds

It only analyses the results produced by the validation engine.

The analyzer accepts the actual WalkForwardValidator result
structure, including:

    training_best
    validation
    metrics
    verdict
    failure_reasons

This fixes the previous data-contract mismatch where the
analyzer expected:

    result["training"]

while WalkForwardValidator actually stored:

    result["training_best"]
"""

from __future__ import annotations


class RobustnessAnalyzer:
    """
    Analyse the robustness of completed walk-forward windows.
    """

    def __init__(
        self,
        results: list[dict],
    ):

        self.results = results

    # =====================================================
    # NUMERIC HELPER
    # =====================================================

    @staticmethod
    def _number(
        value,
        default=0.0,
    ):

        try:

            return float(value)

        except (
            TypeError,
            ValueError,
        ):

            return default

    # =====================================================
    # PERFORMANCE SCORE
    # =====================================================

    def performance_score(
        self,
        metrics: dict,
    ):
        """
        Convert one completed result into a 0-100 quality score.

        This is an analytical score only.

        It is deliberately separate from ValidationMetrics'
        PASS / FAIL classification.

        Score components:

            Profit          30
            Profit Factor   30
            Trade Sample    20
            Win Rate        20
        """

        if not isinstance(metrics, dict):

            return 0.0

        profit = self._number(
            metrics.get(
                "profit",
                metrics.get(
                    "net_profit",
                    0.0,
                ),
            ),
        )

        profit_factor = self._number(
            metrics.get(
                "profit_factor",
                0.0,
            ),
        )

        trades = self._number(
            metrics.get(
                "total_trades",
                metrics.get(
                    "trades",
                    0,
                ),
            ),
        )

        win_rate = self._number(
            metrics.get(
                "win_rate",
                0.0,
            ),
        )

        score = 0.0

        # -------------------------------------------------
        # PROFIT
        # -------------------------------------------------

        if profit > 0:

            score += 30

        # -------------------------------------------------
        # PROFIT FACTOR
        # -------------------------------------------------

        if profit_factor >= 2.0:

            score += 30

        elif profit_factor >= 1.5:

            score += 20

        elif profit_factor >= 1.0:

            score += 10

        # -------------------------------------------------
        # TRADE SAMPLE
        #
        # This is an analytical reliability contribution.
        # It does NOT independently cause validation failure.
        # -------------------------------------------------

        if trades >= 100:

            score += 20

        elif trades >= 50:

            score += 15

        elif trades >= 20:

            score += 10

        elif trades >= 10:

            score += 5

        # -------------------------------------------------
        # WIN RATE
        # -------------------------------------------------

        if win_rate >= 50:

            score += 20

        elif win_rate >= 35:

            score += 10

        return min(
            round(score, 2),
            100.0,
        )

    # =====================================================
    # EXTRACT TRAINING METRICS
    # =====================================================

    def _training_metrics(
        self,
        result: dict,
    ):
        """
        Extract the optimiser's winning training configuration.

        WalkForwardValidator stores this under:

            training_best

        Older result formats may use:

            training

        Both are supported.
        """

        if not isinstance(result, dict):

            return {}

        training = result.get(
            "training_best",
        )

        if isinstance(
            training,
            dict,
        ):

            return training

        training = result.get(
            "training",
        )

        if isinstance(
            training,
            dict,
        ):

            return training

        return {}

    # =====================================================
    # EXTRACT VALIDATION METRICS
    # =====================================================

    def _validation_metrics(
        self,
        result: dict,
    ):
        """
        Extract validation metrics.

        Preferred source:

            result["metrics"]

        Fallback:

            result["validation"]
        """

        if not isinstance(result, dict):

            return {}

        metrics = result.get(
            "metrics",
        )

        if isinstance(
            metrics,
            dict,
        ):

            return metrics

        validation = result.get(
            "validation",
        )

        if isinstance(
            validation,
            dict,
        ):

            return validation

        return {}

    # =====================================================
    # STABILITY SCORE
    # =====================================================

    def stability_score(
        self,
    ):
        """
        Measure consistency across validation windows.

        Stability is based on the validation performance score
        for each window.

        A strategy that performs reasonably across many windows
        receives a higher stability score than one dependent on
        a single exceptional window.

        A zero-performance window receives a penalty.

        This is intentionally independent of the individual
        ValidationMetrics robustness score.
        """

        scores = []

        for result in self.results:

            metrics = self._validation_metrics(
                result
            )

            score = self.performance_score(
                metrics
            )

            scores.append(
                score
            )

        if not scores:

            return 0.0

        average = (
            sum(scores)
            /
            len(scores)
        )

        failures = sum(
            1
            for score in scores
            if score <= 0
        )

        penalty = (
            failures * 15
        )

        return max(
            0.0,
            round(
                average - penalty,
                2,
            ),
        )

    # =====================================================
    # COMPLETE ANALYSIS
    # =====================================================

    def analyse(self):
        """
        Produce the complete robustness report.
        """

        training_scores = []

        validation_scores = []

        # -------------------------------------------------
        # Analyse every window
        # -------------------------------------------------

        for result in self.results:

            training = self._training_metrics(
                result
            )

            validation = self._validation_metrics(
                result
            )

            training_scores.append(
                self.performance_score(
                    training
                )
            )

            validation_scores.append(
                self.performance_score(
                    validation
                )
            )

        # -------------------------------------------------
        # Training quality
        # -------------------------------------------------

        if training_scores:

            training_quality = (
                sum(training_scores)
                /
                len(training_scores)
            )

        else:

            training_quality = 0.0

        # -------------------------------------------------
        # Validation quality
        # -------------------------------------------------

        if validation_scores:

            validation_quality = (
                sum(validation_scores)
                /
                len(validation_scores)
            )

        else:

            validation_quality = 0.0

        # -------------------------------------------------
        # Stability
        # -------------------------------------------------

        stability = self.stability_score()

        # -------------------------------------------------
        # Final robustness
        #
        # Validation performance carries the greatest weight
        # because unseen data is the most important evidence.
        # -------------------------------------------------

        final_score = round(
            (
                validation_quality * 0.50
                +
                stability * 0.30
                +
                training_quality * 0.20
            ),
            2,
        )

        # -------------------------------------------------
        # Verdict
        # -------------------------------------------------

        if final_score >= 75:

            verdict = "PASS"

        elif final_score >= 50:

            verdict = "REVIEW"

        else:

            verdict = "REJECT"

        return {

            "training_quality":
                round(
                    training_quality,
                    2,
                ),

            "validation_quality":
                round(
                    validation_quality,
                    2,
                ),

            "stability":
                stability,

            "robustness_score":
                final_score,

            "verdict":
                verdict,

            "training_window_scores":
                [
                    round(
                        score,
                        2,
                    )
                    for score
                    in training_scores
                ],

            "validation_window_scores":
                [
                    round(
                        score,
                        2,
                    )
                    for score
                    in validation_scores
                ],
        }

    # =====================================================
    # DISPLAY
    # =====================================================

    def display(self):

        report = self.analyse()

        print()

        print(
            "=" * 50
        )

        print(
            "ATLAS ROBUSTNESS ANALYSIS"
        )

        print(
            "=" * 50
        )

        print()

        print(
            f"Training Quality: "
            f"{report['training_quality']}/100"
        )

        print(
            f"Validation Quality: "
            f"{report['validation_quality']}/100"
        )

        print(
            f"Stability Score: "
            f"{report['stability']}/100"
        )

        print()

        print(
            "Training Window Scores:"
        )

        for number, score in enumerate(
            report[
                "training_window_scores"
            ],
            start=1,
        ):

            print(
                f"  Window {number}: "
                f"{score}/100"
            )

        print()

        print(
            "Validation Window Scores:"
        )

        for number, score in enumerate(
            report[
                "validation_window_scores"
            ],
            start=1,
        ):

            print(
                f"  Window {number}: "
                f"{score}/100"
            )

        print()

        print(
            f"ROBUSTNESS SCORE: "
            f"{report['robustness_score']}/100"
        )

        print()

        print(
            f"VERDICT: "
            f"{report['verdict']}"
        )

        print(
            "=" * 50
        )