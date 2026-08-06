"""
Atlas AI Trading Platform 4.0

Parallel Optimisation Runner

Handles optimiser configurations.

Supports:
- dict configurations
- tuple configurations

"""

from __future__ import annotations


from concurrent.futures import ProcessPoolExecutor, as_completed


from backtesting.engine import BacktestEngine



# =========================================================
# NORMALISE CONFIGURATION
# =========================================================

def normalise_configuration(configuration):


    if isinstance(configuration, dict):

        return configuration



    if isinstance(configuration, tuple):

        return {

            "score_threshold":
                configuration[0],

            "confidence":
                configuration[1],

            "atr_stop":
                configuration[2],

            "atr_target":
                configuration[3],

        }



    raise TypeError(

        f"Unsupported configuration type: {type(configuration)}"

    )





# =========================================================
# WORKER
# =========================================================

def run_configuration(

    configuration,

    dataframe,

    symbol,

    starting_cash,

):


    try:


        configuration = normalise_configuration(

            configuration

        )



        engine = BacktestEngine(


            starting_cash=starting_cash,


            minimum_score=

                configuration.get(

                    "score_threshold",

                    60

                ),



            minimum_confidence=

                configuration.get(

                    "confidence",

                    0.60

                ),



            atr_stop=

                configuration.get(

                    "atr_stop",

                    2.0

                ),



            atr_target=

                configuration.get(

                    "atr_target",

                    4.0

                ),


        )



        result = engine.run(

            symbol=symbol,

            dataframe=dataframe,

        )



        simulator = result.get(

            "simulator_results",

            {}

        )



        return {


            **configuration,


            "net_profit":

                result.get(

                    "net_profit",

                    0

                ),



            "profit_factor":

                simulator.get(

                    "profit_factor",

                    0

                ),



            "win_rate":

                simulator.get(

                    "win_rate",

                    0

                ),



            "trade_count":

                len(

                    result.get(

                        "trade_list",

                        []

                    )

                ),



            "result":

                result,

        }



    except Exception as error:


        return {


            "error":

                str(error),


            "net_profit":

                -999999,


        }





# =========================================================
# PARALLEL OPTIMIZER
# =========================================================

class ParallelOptimizer:


    def __init__(

        self,

        workers: int = 16,

        use_regime_filter: bool = True,

    ):


        self.workers = workers

        self.use_regime_filter = use_regime_filter





    def run(

        self,

        dataframe,

        symbol,

        starting_cash,

        configurations,

    ):


        print()

        print(

            f"Running {len(configurations)} tests using {self.workers} workers"

        )



        results = []



        with ProcessPoolExecutor(

            max_workers=self.workers

        ) as executor:



            futures = []


            for configuration in configurations:


                futures.append(

                    executor.submit(

                        run_configuration,

                        configuration,

                        dataframe,

                        symbol,

                        starting_cash,

                    )

                )



            for future in as_completed(futures):


                results.append(

                    future.result()

                )



        return results