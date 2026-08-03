"""
Atlas AI Trading Platform 3.3

Strategy Optimisation Engine

Features:

- Parameter search
- Parallel backtesting
- Robust ranking
- Dataset caching
- Result persistence
- Best configuration reporting
"""


from __future__ import annotations


from research.dataset_cache import DatasetCache

from optimisation.parallel_runner import ParallelOptimizer

from optimisation.results_database import OptimisationDatabase



class StrategyOptimizer:


    def __init__(
        self,
        symbol: str = "SPY",
        starting_cash: float = 100000.0,
        use_regime_filter: bool = True,
    ):


        self.symbol = symbol

        self.starting_cash = starting_cash

        self.use_regime_filter = use_regime_filter


        self.results = []


        self.cache = DatasetCache()


        self.database = OptimisationDatabase()



    # =====================================================
    # Ranking
    # =====================================================

    def calculate_score(
        self,
        result: dict,
    ):


        profit = result.get(
            "net_profit",
            0
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
            0
        )


        score = 0



        score += (

            profit

            /

            self.starting_cash

            *

            100

            *

            30

        )



        score += min(

            profit_factor,

            4

        ) * 20



        score += min(

            win_rate,

            70

        ) * 0.15



        if trades >= 200:

            score += 20


        elif trades >= 100:

            score += 15


        elif trades >= 50:

            score += 10


        elif trades >= 20:

            score += 5


        else:

            score -= 20



        if profit_factor > 6 and trades < 100:

            score -= 20


        if profit_factor > 10:

            score -= 30



        return round(

            score,

            2

        )



    # =====================================================
    # Generate Search Space
    # =====================================================

    def generate_configurations(self):


        configurations = []


        scores = [
            40,
            50,
            60,
            70,
            80,
        ]


        confidences = [
            0.4,
            0.5,
            0.6,
            0.7,
        ]


        atr_stops = [
            3.0,
            3.5,
            3.75,
            4.0,
            4.25,
        ]


        atr_targets = [
            4.0,
            4.5,
            5.0,
            5.5,
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

                                target,

                            )

                        )


        return configurations



    # =====================================================
    # Run Optimisation
    # =====================================================

    def optimise(
        self,
        symbol: str | None = None,
    ):


        if symbol:

            self.symbol = symbol



        print()

        print(
            f"Loading dataset {self.symbol}"
        )

        print()



        dataset = self.cache.load(

            self.symbol

        )



        configs = self.generate_configurations()



        print(

            f"Testing {len(configs)} configurations"

        )



        runner = ParallelOptimizer(

            use_regime_filter=self.use_regime_filter

        )



        results = runner.run(

            dataset,

            self.symbol,

            self.starting_cash,

            configs,

        )



        self.results = []



        for result in results:


            if result.get(

                "total_trades",

                0

            ) < 10:

                continue



            result["ranking_score"] = self.calculate_score(

                result

            )



            self.database.save_result(

                self.symbol,

                result,

            )



            self.results.append(

                result

            )



        self.results.sort(

            key=lambda x:

            x.get(

                "ranking_score",

                0

            ),

            reverse=True,

        )



        return self.results



    # =====================================================
    # Compatibility Alias
    # =====================================================

    def run(
        self,
        symbol: str | None = None,
    ):

        return self.optimise(

            symbol

        )



    # =====================================================
    # Display
    # =====================================================

    def display(
        self,
        count: int = 10,
    ):


        print()

        print(
            "BEST CONFIGURATIONS"
        )

        print(
            "==================="
        )


        for i, result in enumerate(

            self.results[:count],

            start=1,

        ):


            print()

            print(

                f"{i}. "

                f"Profit ${result.get('net_profit',0):.2f} "

                f"| PF {result.get('profit_factor',0)}"

            )


            print(

                f"   Score {result.get('score_threshold')} "

                f"| Confidence {result.get('confidence')} "

                f"| ATR "

                f"{result.get('atr_stop')}/"

                f"{result.get('atr_target')}"

            )


            print(

                f"   Ranking {result.get('ranking_score')}"

            )