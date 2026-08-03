"""
Atlas AI Trading Platform 3.3

Walk Forward Validation Engine

Workflow:

Training Data
        |
Optimisation
        |
Locked Parameters
        |
Unseen Validation
        |
Validation Report
"""


from __future__ import annotations


from optimisation.parallel_runner import ParallelOptimizer
from optimisation.optimizer import StrategyOptimizer

from backtesting.engine import BacktestEngine

from validation.window import WindowGenerator
from validation.metrics import ValidationMetrics

from database.validation import ValidationDatabase

from research.regime_detector import RegimeDetector



class WalkForwardValidator:


    def __init__(
        self,
        symbol: str = "SPY",
        starting_cash: float = 100000.0,
        training_size: int = 500,
        validation_size: int = 100,
        step_size: int = 100,
        expanding: bool = True,
        max_windows: int | None = None,
    ):


        self.symbol = symbol

        self.starting_cash = starting_cash

        self.max_windows = max_windows


        self.optimizer = StrategyOptimizer(
            symbol=symbol,
            starting_cash=starting_cash,
        )


        self.parallel_runner = ParallelOptimizer(
            use_regime_filter=True
        )


        self.backtester = BacktestEngine(
            starting_cash=starting_cash,
            use_regime_filter=True,
        )


        self.window_generator = WindowGenerator(
            training_size=training_size,
            validation_size=validation_size,
            step_size=step_size,
            expanding=expanding,
        )


        self.database = ValidationDatabase()

        self.regime_detector = RegimeDetector()


        self.results = []



    # =====================================================
    # RUN VALIDATION
    # =====================================================

    def run(self):


        print()

        print(
            "Loading validation dataset..."
        )


        dataset = self.optimizer.cache.load(
            self.symbol
        )


        windows = self.window_generator.generate(
            dataset
        )


        if self.max_windows:

            windows = windows[:self.max_windows]


        print()

        print(
            f"Windows Generated: {len(windows)}"
        )


        self.results = []


        for number, window in enumerate(
            windows,
            start=1,
        ):


            print()

            print("=" * 60)

            print(
                f"WALK FORWARD WINDOW {number}"
            )

            print("=" * 60)



            result = self.validate_window(
                window
            )


            self.results.append(
                result
            )


            self.database.save(
                self.symbol,
                result,
            )


        return self.results



    # =====================================================
    # VALIDATE SINGLE WINDOW
    # =====================================================

    def validate_window(
        self,
        window,
    ):


        print()

        print(
            "Optimising training period..."
        )



        configs = self.optimizer.generate_configurations()



        training_results = self.parallel_runner.run(
            window.training,
            self.symbol,
            self.starting_cash,
            configs,
        )



        if not training_results:


            return {
                "verdict": "FAIL",
                "reason": "NO_TRAINING_RESULTS"
            }



        for result in training_results:


            result["ranking_score"] = (
                self.optimizer.calculate_score(
                    result
                )
            )



        best = max(
            training_results,
            key=lambda x:
            x.get(
                "ranking_score",
                0
            )
        )



        parameters = {


            "score_threshold":

                best.get(
                    "score_threshold",
                    40
                ),


            "confidence":

                best.get(
                    "confidence",
                    0.4
                ),


            "atr_stop":

                best.get(
                    "atr_stop",
                    4.0
                ),


            "atr_target":

                best.get(
                    "atr_target",
                    5.0
                ),

        }



        print()

        print(
            "LOCKED PARAMETERS"
        )

        print(
            parameters
        )



        print()

        print(
            "Testing unseen validation data..."
        )



        validation = self.backtester.run(

            window.validation,

            score_threshold=
                parameters["score_threshold"],

            confidence_threshold=
                parameters["confidence"],

            atr_stop=
                parameters["atr_stop"],

            atr_target=
                parameters["atr_target"],

        )



        regime = self.regime_detector.analyse(
            window.validation
        )



        training_metrics = (
            ValidationMetrics.from_result(
                best
            )
        )


        validation_metrics = (
            ValidationMetrics.from_result(
                validation
            )
        )



        verdict = (

            "PASS"

            if validation_metrics.passes()

            else

            "FAIL"

        )



        print()

        print(
            f"RESULT: {verdict}"
        )



        return {


            "window":

                str(window),


            "parameters":

                parameters,


            "training":

                training_metrics.to_dict(),


            "validation":

                validation_metrics.to_dict(),


            "regime":

                regime,


            "verdict":

                verdict,

        }