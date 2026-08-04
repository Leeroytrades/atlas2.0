"""
Atlas AI Trading Platform 3.6

Parallel Optimisation Runner

Runs multiple backtest configurations
using multiprocessing.

Supports:

- BacktestResult objects
- Metadata attachment
- Walk-forward validation
- Regime-aware strategies
"""

from __future__ import annotations


import os

from concurrent.futures import (
    ProcessPoolExecutor,
    as_completed,
)


from backtesting.engine import BacktestEngine





# =====================================================
# Single Configuration Worker
# =====================================================

def run_configuration(

    dataset,

    symbol: str,

    starting_cash: float,

    score_threshold: int,

    confidence: float,

    atr_stop: float,

    atr_target: float,

    use_regime_filter: bool = True,

):


    engine = BacktestEngine(

        starting_cash=starting_cash,

        use_regime_filter=use_regime_filter,

    )



    result = engine.run(

        dataset,

        score_threshold=int(
            score_threshold
        ),

        confidence_threshold=float(
            confidence
        ),

        atr_stop=float(
            atr_stop
        ),

        atr_target=float(
            atr_target
        ),

    )



    # ---------------------------------
    # Convert result object to dict
    # ---------------------------------

    if hasattr(
        result,
        "to_dict"
    ):

        results = result.to_dict()


    else:

        results = dict(
            result
        )



    # ---------------------------------
    # Attach configuration metadata
    # ---------------------------------

    results.update(

        {


            "score_threshold":

                score_threshold,


            "confidence":

                confidence,


            "atr_stop":

                atr_stop,


            "atr_target":

                atr_target,

        }

    )



    return results





# =====================================================
# Parallel Optimiser
# =====================================================

class ParallelOptimizer:



    def __init__(

        self,

        workers: int | None = None,

        use_regime_filter: bool = True,

    ):


        self.workers = (

            workers

            or

            os.cpu_count()

            or

            1

        )


        self.use_regime_filter = (

            use_regime_filter

        )





    # =================================================
    # Run Optimisation Grid
    # =================================================

    def run(

        self,

        dataset,

        symbol: str,

        starting_cash: float,

        configurations: list[tuple],

    ) -> list[dict]:


        results = []


        total = len(
            configurations
        )



        print()

        print(

            f"Running {total} tests "

            f"using {self.workers} workers"

        )

        print()



        with ProcessPoolExecutor(

            max_workers=self.workers

        ) as executor:



            futures = []



            for config in configurations:



                future = executor.submit(

                    run_configuration,

                    dataset,

                    symbol,

                    starting_cash,

                    config[0],

                    config[1],

                    config[2],

                    config[3],

                    self.use_regime_filter,

                )


                futures.append(
                    future
                )



            completed = 0



            for future in as_completed(

                futures

            ):


                result = future.result()



                results.append(

                    result

                )



                completed += 1



                print(

                    f"Completed {completed}/{total}"

                )



        return results