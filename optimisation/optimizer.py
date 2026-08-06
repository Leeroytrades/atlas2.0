"""
Atlas AI Trading Platform 4.0

Strategy Optimiser

Searches parameter combinations
and ranks strategies using:

- Profit
- Profit Factor
- Drawdown control
- Trade quality
- Stability
"""

from __future__ import annotations


from itertools import product

from optimisation.parallel_runner import ParallelOptimizer



class StrategyOptimizer:


    def __init__(

        self,

        starting_cash: float = 100000.0,

    ):


        self.starting_cash = starting_cash


        self.parallel_runner = ParallelOptimizer()



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


        #
        # Development defaults
        #
        # 5 x 3 x 2 x 4 = 120 tests
        #
        # Increase later for full research runs
        #


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

                    "score_threshold":

                        score,


                    "confidence":

                        confidence,


                    "atr_stop":

                        atr_stop,


                    "atr_target":

                        atr_target,

                }

            )



        print()

        print(

            f"Generated {len(configurations)} optimisation configurations"

        )


        return configurations





    # =====================================================
    # SCORE RESULT
    # =====================================================

    def calculate_score(

        self,

        result: dict,

    ):


        profit = result.get(

            "profit",

            result.get(

                "net_profit",

                0

            )

        )


        profit_factor = result.get(

            "profit_factor",

            0

        )


        win_rate = result.get(

            "win_rate",

            0

        )


        trades = result.get(

            "total_trades",

            result.get(

                "trades",

                0

            )

        )


        drawdown = result.get(

            "max_drawdown",

            0

        )



        score = 0



        # =====================================
        # PROFIT
        # =====================================

        score += (

            profit

            /

            self.starting_cash

            *

            100

            *

            5

        )



        # =====================================
        # PROFIT FACTOR
        # =====================================

        if profit_factor >= 2:

            score += 30


        elif profit_factor >= 1.5:

            score += 20


        elif profit_factor >= 1:

            score += 5


        else:

            score -= 50




        # =====================================
        # DRAWDOWN
        # =====================================

        if drawdown <= 10:

            score += 30


        elif drawdown <= 20:

            score += 10


        elif drawdown > 40:

            score -= 100


        elif drawdown > 25:

            score -= 60




        # =====================================
        # TRADE QUALITY
        # =====================================

        if 50 <= trades <= 300:

            score += 15


        elif trades < 30:

            score -= 40


        elif trades > 500:

            score -= 50




        # =====================================
        # WIN RATE
        # =====================================

        if win_rate >= 40:

            score += 10


        elif win_rate < 25:

            score -= 20




        # =====================================
        # OVERFIT PROTECTION
        # =====================================

        if profit > 0 and drawdown > 50:

            score -= 150


        if profit_factor > 10:

            score -= 50



        return round(

            score,

            2

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


            configurations = self.generate_configurations()



        print()

        print(

            f"Running {len(configurations)} optimisation tests"

        )



        results = self.parallel_runner.run(

            dataset,

            symbol,

            self.starting_cash,

            configurations,

        )



        for result in results:


            result["ranking_score"] = self.calculate_score(

                result

            )



        results.sort(

            key=lambda x:

                x.get(

                    "ranking_score",

                    0

                ),

            reverse=True,

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



        return results[0]