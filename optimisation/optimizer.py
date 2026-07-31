"""
Atlas AI Trading Platform 3.0

Strategy Optimiser

Searches Atlas strategy parameters.

Optimises:

- Score threshold
- Confidence threshold
- ATR stop
- ATR target

Ranks using:

- Profit
- Profit factor
- Win rate
- Trade reliability
"""

from __future__ import annotations


from backtesting.engine import BacktestEngine





class StrategyOptimizer:


    def __init__(
        self,
        symbol: str = "SPY",
        starting_cash: float = 100000.0,
    ):

        self.symbol = symbol

        self.starting_cash = starting_cash

        self.results = []





    def calculate_score(
        self,
        result: dict,
    ):


        profit = result["net_profit"]

        win_rate = result["win_rate"]

        profit_factor = result["profit_factor"]

        trades = result["total_trades"]



        score = 0



        score += (

            profit

            /

            self.starting_cash

            *

            100

            *

            40

        )



        score += (

            win_rate

            *

            0.20

        )



        if isinstance(

            profit_factor,

            (float, int)

        ):

            score += min(

                profit_factor,

                5

            ) * 10



        if trades >= 50:

            score += 10


        elif trades >= 20:

            score += 5


        else:

            score -= 10



        return round(

            score,

            2

        )





    def optimise(
        self,
        symbol: str | None = None,
    ):


        if symbol is not None:

            self.symbol = symbol



        self.results = []



        configurations = []



        scores = [

            50,
            60,
            70,
            80,
            90,
            100,
            110,
            120,

        ]


        confidences = [

            0.5,
            0.6,
            0.7,
            0.8,
            0.9,
            1.0,

        ]


        atr_stops = [

            1.5,
            2.0,
            2.5,
            3.0,

        ]


        atr_targets = [

            3.0,
            4.0,
            5.0,
            6.0,

        ]



        for score in scores:

            for confidence in confidences:

                for stop in atr_stops:

                    for target in atr_targets:

                        configurations.append(

                            (

                                score,

                                confidence,

                                stop,

                                target

                            )

                        )



        total = len(

            configurations

        )



        for number, config in enumerate(

            configurations,

            start=1

        ):



            score_threshold, confidence, atr_stop, atr_target = config



            print(

                f"Testing {number}/{total}: "

                f"Score {score_threshold} "

                f"Confidence {confidence} "

                f"ATR {atr_stop}/{atr_target}"

            )



            engine = BacktestEngine(

                self.starting_cash

            )



            result = engine.run(

                self.symbol,

                score_threshold,

                confidence,

                atr_stop,

                atr_target,

            )



            if result["total_trades"] < 10:

                continue



            ranking_score = self.calculate_score(

                result

            )



            self.results.append(

                {

                    "ranking_score": ranking_score,

                    "score_threshold": score_threshold,

                    "confidence": confidence,

                    "atr_stop": atr_stop,

                    "atr_target": atr_target,

                    **result,

                }

            )



        self.results = sorted(

            self.results,

            key=lambda x: x["ranking_score"],

            reverse=True

        )


        return self.results





    def display(
        self,
        count: int = 10,
    ):


        print()

        print(

            "Best Configurations"

        )

        print(

            "------------------"

        )



        for index, result in enumerate(

            self.results[:count],

            start=1

        ):


            print()

            print(

                f"{index}. "

                f"Atlas Score {result['ranking_score']}"

            )


            print(

                f"   Profit ${result['net_profit']} "

                f"| Win Rate {result['win_rate']}% "

                f"| PF {result['profit_factor']}"

            )


            print(

                f"   Score {result['score_threshold']} "

                f"| Confidence {result['confidence']} "

                f"| ATR "

                f"{result['atr_stop']}/"

                f"{result['atr_target']}"

            )