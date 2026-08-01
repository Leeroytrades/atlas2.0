"""
Atlas AI Trading Platform 3.3

Walk Forward Validator

Professional strategy validation.

Process:

1. Split historical data
2. Optimise on training period
3. Test on unseen validation period
4. Compare results
5. Produce verdict
"""

from __future__ import annotations


import pandas as pd


from optimisation.optimizer import StrategyOptimizer

from backtesting.engine import BacktestEngine



class WalkForwardValidator:


    def __init__(
        self,
        starting_cash: float = 100000.0,
        train_ratio: float = 0.7,
    ):


        self.starting_cash = starting_cash

        self.train_ratio = train_ratio



    # =====================================================
    # Split Dataset
    # =====================================================

    def split_data(
        self,
        dataframe: pd.DataFrame,
    ):


        split = int(

            len(dataframe)

            *

            self.train_ratio

        )


        training = dataframe.iloc[

            :split

        ].copy()



        validation = dataframe.iloc[

            split:

        ].copy()



        return training, validation



    # =====================================================
    # Validate
    # =====================================================

    def run(
        self,
        symbol: str,
        dataframe: pd.DataFrame,
    ):


        print()

        print(
            "==============================="
        )

        print(
            " Atlas Walk Forward Validation"
        )

        print(
            "==============================="
        )


        training, validation = self.split_data(

            dataframe

        )


        print()

        print(
            f"Training candles: {len(training)}"
        )

        print(
            f"Validation candles: {len(validation)}"
        )



        # ---------------------------------
        # Optimise training period
        # ---------------------------------

        print()

        print(
            "Optimising training data..."
        )


        optimizer = StrategyOptimizer(

            symbol,

            self.starting_cash

        )


        train_results = optimizer.optimise()



        if not train_results:


            return {

                "verdict":
                    "FAILED",

                "reason":
                    "No training results"

            }



        best = train_results[0]



        print()

        print(
            "Best Training Parameters:"
        )


        print(

            f"Score {best['score_threshold']} "

            f"| Confidence {best['confidence']} "

            f"| ATR "

            f"{best['atr_stop']}/"

            f"{best['atr_target']}"

        )



        # ---------------------------------
        # Validate unseen data
        # ---------------------------------


        print()

        print(
            "Testing unseen validation data..."
        )



        engine = BacktestEngine(

            self.starting_cash

        )



        validation_result = engine.run(

            validation,

            best["score_threshold"],

            best["confidence"],

            best["atr_stop"],

            best["atr_target"],

        )



        print()

        print(
            "==============================="
        )

        print(
            " RESULTS"
        )

        print(
            "==============================="
        )



        print()

        print(
            "TRAINING"
        )

        print(
            f"Profit: ${best['net_profit']}"
        )

        print(
            f"PF: {best['profit_factor']}"
        )

        print(
            f"Win Rate: {best['win_rate']}%"
        )



        print()

        print(
            "VALIDATION"
        )

        print(
            f"Profit: ${validation_result['net_profit']}"
        )

        print(
            f"PF: {validation_result['profit_factor']}"
        )

        print(
            f"Win Rate: {validation_result['win_rate']}%"
        )



        # ---------------------------------
        # Verdict
        # ---------------------------------


        if (

            validation_result["net_profit"] > 0

            and

            validation_result["profit_factor"] >= 1.2

        ):

            verdict = "PASS"


        else:

            verdict = "FAIL"



        print()

        print(
            f"VERDICT: {verdict}"
        )



        return {


            "verdict":

                verdict,


            "parameters":

                {

                    "score_threshold":
                        best["score_threshold"],

                    "confidence":
                        best["confidence"],

                    "atr_stop":
                        best["atr_stop"],

                    "atr_target":
                        best["atr_target"],

                },


            "training":

                best,


            "validation":

                validation_result,

        }