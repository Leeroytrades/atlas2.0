"""
Atlas AI Trading Platform 3.2

Strategy Optimiser

Smart quantitative research engine.

Features:

- Cached datasets
- Multiprocessing optimisation
- SQLite experiment storage
- Intelligent parameter search
- Risk adjusted ranking
- Reduced redundant testing
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
    ):

        self.symbol = symbol

        self.starting_cash = starting_cash

        self.results = []

        self.cache = DatasetCache()

        self.database = OptimisationDatabase()



    # =====================================================
    # Ranking System
    # =====================================================

    def calculate_score(
        self,
        result: dict,
    ):


        profit = result.get(
            "net_profit",
            0
        )


        win_rate = result.get(
            "win_rate",
            0
        )


        profit_factor = result.get(
            "profit_factor",
            0
        )


        trades = result.get(
            "total_trades",
            0
        )


        score = 0



        # Profit contribution

        score += (

            profit

            /

            self.starting_cash

            *

            100

            *

            35

        )



        # Win rate

        score += (

            win_rate

            *

            0.25

        )



        # Profit factor

        if isinstance(
            profit_factor,
            (int,float)
        ):

            score += (

                min(
                    profit_factor,
                    5
                )

                *

                20

            )



        # Trade quantity reliability

        if trades >= 100:

            score += 15


        elif trades >= 50:

            score += 10


        elif trades >= 20:

            score += 5


        else:

            score -= 10



        return round(
            score,
            2
        )



    # =====================================================
    # Smart Parameter Generator
    # =====================================================

    def generate_configurations(
        self,
    ):


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



        dataset = self.cache.load(

            self.symbol

        )



        print(
            f"Dataset rows: {len(dataset)}"
        )



        configurations = self.generate_configurations()



        print()

        print(
            f"Configurations: {len(configurations)}"
        )



        runner = ParallelOptimizer()



        results = runner.run(

            dataset,

            self.symbol,

            self.starting_cash,

            configurations,

        )



        self.results = []



        for result in results:



            if result.get(
                "total_trades",
                0
            ) < 10:

                continue



            result["ranking_score"] = (

                self.calculate_score(
                    result
                )

            )



            self.database.save_result(

                self.symbol,

                result,

            )


            self.results.append(

                result

            )



        self.results = sorted(

            self.results,

            key=lambda x:

                x["ranking_score"],

            reverse=True,

        )


        return self.results



    # =====================================================
    # Display
    # =====================================================

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

            start=1,

        ):



            print()



            print(

                f"{index}. "

                f"Profit ${result.get('net_profit',0):.2f} "

                f"| Win Rate "

                f"{result.get('win_rate',0)}% "

                f"| PF "

                f"{result.get('profit_factor',0)}"

            )



            print(

                "   "

                f"Score {result.get('score_threshold')} "

                f"| Confidence "

                f"{result.get('confidence')} "

                f"| ATR "

                f"{result.get('atr_stop')}/"

                f"{result.get('atr_target')}"

            )



            print(

                "   "

                f"Ranking Score: "

                f"{result.get('ranking_score')}"

            )