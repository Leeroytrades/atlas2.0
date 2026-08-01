"""
Atlas AI Trading Platform 3.0

Parallel Optimisation Runner

Runs multiple strategy configurations
across available CPU cores.
"""

from __future__ import annotations


from concurrent.futures import ProcessPoolExecutor, as_completed

import os


from optimisation.worker import run_configuration



class ParallelOptimizer:



    def __init__(
        self,
        workers: int | None = None,
    ):

        self.workers = workers or os.cpu_count() or 1



    def run(
        self,
        dataset,
        symbol: str,
        starting_cash: float,
        configurations: list[tuple],
    ) -> list[dict]:
        """
        Execute optimisation configurations
        in parallel.
        """


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