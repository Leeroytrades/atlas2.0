"""
Atlas AI Trading Platform 4.0

Walk Forward Validation Engine

Workflow:

Historical Data
        |
Create Windows
        |
Optimise Training Window
        |
Lock Parameters
        |
Run Unseen Validation Window
        |
Compare Results
        |
PASS / FAIL
"""

from __future__ import annotations


from data.market_data import MarketData

from indicators.composite import build_indicator_set

from optimisation.optimizer import StrategyOptimizer

from backtesting.engine import BacktestEngine

from validation.window import WindowGenerator

from validation.metrics import ValidationMetrics

from database.validation import ValidationDatabase

from research.regime_detector import RegimeDetector



class WalkForwardValidator:


    def __init__(

        self,

        symbol="SPY",

        starting_cash=100000.0,

        training_size=1000,

        validation_size=250,

        step_size=250,

        expanding=True,

        max_windows=None,

    ):


        self.symbol = symbol

        self.starting_cash = starting_cash

        self.max_windows = max_windows


        self.market = MarketData()


        self.optimizer = StrategyOptimizer(

            starting_cash=starting_cash

        )


        self.window_generator = WindowGenerator(

            training_size=training_size,

            validation_size=validation_size,

            step_size=step_size,

            expanding=expanding,

        )


        self.database = ValidationDatabase()


        self.regime_detector = RegimeDetector()



    # =====================================================
    # LOAD DATA
    # =====================================================

    def load_data(self):


        dataframe = self.market.get_history(

            symbol=self.symbol,

            period="10y",

            interval="1d",

        )


        dataframe = build_indicator_set(

            dataframe.copy()

        )


        print()

        print(

            f"Dataset candles available: {len(dataframe)}"

        )


        return dataframe



    # =====================================================
    # RUN
    # =====================================================

    def run(self):


        dataframe = self.load_data()


        windows = self.window_generator.generate(

            dataframe

        )


        if self.max_windows:

            windows = windows[:self.max_windows]


        print()

        print(

            f"Windows Generated: {len(windows)}"

        )


        results=[]



        for number, window in enumerate(

            windows,

            start=1

        ):


            print()

            print("="*60)

            print(

                f"WALK FORWARD WINDOW {number}"

            )

            print("="*60)



            result = self.validate_window(

                window

            )


            results.append(result)


            try:

                self.database.save(

                    self.symbol,

                    result

                )

            except Exception:

                pass



        return results



    # =====================================================
    # VALIDATE WINDOW
    # =====================================================

    def validate_window(

        self,

        window

    ):


        print()

        print(

            "Optimising training period..."

        )



        training_results = self.optimizer.optimise(

            window.training,

            self.symbol

        )



        if not training_results:


            return {

                "verdict":"FAIL",

                "reason":"NO_RESULTS"

            }



        best=max(

            training_results,

            key=lambda x:

            x.get(

                "ranking_score",

                x.get(

                    "profit",

                    0

                )

            )

        )



        parameters={


            "score_threshold":

                best.get(

                    "score_threshold",

                    40

                ),


            "confidence":

                best.get(

                    "confidence",

                    0.40

                ),


            "atr_stop":

                best.get(

                    "atr_stop",

                    3.0

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

        print(parameters)



        print()

        print(

            "Testing unseen validation data..."

        )



        engine=BacktestEngine(

            starting_cash=self.starting_cash,

            minimum_score=parameters["score_threshold"],

            minimum_confidence=parameters["confidence"],

            atr_stop=parameters["atr_stop"],

            atr_target=parameters["atr_target"],

        )



        validation_result=engine.run(

            symbol=self.symbol,

            dataframe=window.validation,

        )



        profit=validation_result.get(

            "net_profit",

            0

        )



        verdict=(

            "PASS"

            if profit > 0

            else

            "FAIL"

        )



        print()

        print(

            f"RESULT: {verdict}"

        )



        return {


            "symbol":

                self.symbol,


            "parameters":

                parameters,


            "validation":

                validation_result,


            "regime":

                self.regime_detector.analyse(

                    window.validation

                ),


            "verdict":

                verdict,

        }



if __name__=="__main__":


    validator=WalkForwardValidator(

        symbol="SPY",

        max_windows=3,

    )


    results=validator.run()


    print()

    print("="*60)

    print("FINAL SUMMARY")

    print("="*60)


    passed=sum(

        1

        for r in results

        if r["verdict"]=="PASS"

    )


    print(

        f"PASS: {passed}/{len(results)}"

    )


    print(

        f"FAIL: {len(results)-passed}/{len(results)}"

    )