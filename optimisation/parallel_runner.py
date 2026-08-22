"""
Atlas AI Trading Platform 4.2

Parallel Optimisation Runner

Handles optimiser configurations in parallel.

Optimisation architecture:

                    Dataset
                       |
                       v
              Parallel Optimizer
                       |
          +------------+------------+
          |            |            |
        Worker       Worker       Worker
          |            |            |
      Configs       Configs       Configs
          |            |            |
          +------------+------------+
                       |
                       v
                  BacktestEngine

Atlas 4.2 improvements:

- Uses the current BacktestEngine interface.
- Does not pass unsupported arguments to BacktestEngine.
- Correctly reads BacktestEngine results.
- Preserves all optimisation configuration parameters.
- Supports dict and tuple configurations.
- Processes configurations in batches.
- Sends the dataframe once per batch.
- Captures worker errors without crashing the full optimisation.
- Correctly identifies zero-trade configurations.
- Preserves the complete backtest result for diagnostics.
"""

from __future__ import annotations

from concurrent.futures import (
    ProcessPoolExecutor,
    as_completed,
)

from backtesting.engine import BacktestEngine
from data.dataset_cache import DatasetCache


# ============================================================
# NORMALISE CONFIGURATION
# ============================================================

def normalise_configuration(configuration):
    """
    Convert supported configuration formats into a dict.

    Supported:

        {
            "score_threshold": 60,
            "confidence": 0.6,
            "atr_stop": 3.0,
            "atr_target": 5.0,
        }

    or:

        (
            60,
            0.6,
            3.0,
            5.0,
        )
    """

    if isinstance(
        configuration,
        dict,
    ):

        return configuration.copy()

    if isinstance(
        configuration,
        tuple,
    ):

        if len(configuration) < 4:

            raise ValueError(
                "Tuple configuration must contain "
                "score_threshold, confidence, "
                "atr_stop and atr_target."
            )

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
        "Unsupported configuration type: "
        f"{type(configuration)}"
    )


# ============================================================
# SINGLE CONFIGURATION
# ============================================================

def run_configuration(
    configuration,
    dataframe,
    symbol,
    starting_cash,
    use_regime_filter=True,
):
    """
    Run one optimisation configuration.

    `use_regime_filter` is retained for compatibility with
    the optimiser architecture.

    The current BacktestEngine performs regime-based strategy
    selection internally through StrategyRunner, so the flag
    is intentionally NOT passed into BacktestEngine.
    """

    configuration = normalise_configuration(
        configuration
    )

    try:

        # ----------------------------------------------------
        # Extract parameters
        # ----------------------------------------------------

        score_threshold = float(
            configuration.get(
                "score_threshold",
                40,
            )
        )

        confidence = float(
            configuration.get(
                "confidence",
                0.40,
            )
        )

        atr_stop = float(
            configuration.get(
                "atr_stop",
                2.0,
            )
        )

        atr_target = float(
            configuration.get(
                "atr_target",
                4.0,
            )
        )

        # ----------------------------------------------------
        # Create current BacktestEngine
        # ----------------------------------------------------

        engine = BacktestEngine(

            starting_cash=
                starting_cash,

            minimum_score=
                score_threshold,

            minimum_confidence=
                confidence,

            atr_stop=
                atr_stop,

            atr_target=
                atr_target,

        )

        # ----------------------------------------------------
        # Run backtest
        # ----------------------------------------------------

        result = engine.run(

            symbol=symbol,

            dataframe=dataframe,

        )

        # ----------------------------------------------------
        # Protect against unexpected result types
        # ----------------------------------------------------

        if not isinstance(
            result,
            dict,
        ):

            return {

                **configuration,

                "ranking_score":
                    -1000000.0,

                "net_profit":
                    0.0,

                "profit":
                    0.0,

                "profit_factor":
                    0.0,

                "win_rate":
                    0.0,

                "trade_count":
                    0,

                "total_trades":
                    0,

                "max_drawdown":
                    999999.0,

                "average_trade":
                    0.0,

                "trade_list":
                    [],

                "valid":
                    False,

                "error":
                    "BacktestEngine returned "
                    "non-dict result",

                "result":
                    result,

            }

        # ----------------------------------------------------
        # Current BacktestEngine returns these fields
        # directly.
        # ----------------------------------------------------

        profit = float(
            result.get(
                "profit",
                result.get(
                    "net_profit",
                    0.0,
                ),
            )
        )

        net_profit = float(
            result.get(
                "net_profit",
                profit,
            )
        )

        profit_factor = float(
            result.get(
                "profit_factor",
                0.0,
            )
        )

        win_rate = float(
            result.get(
                "win_rate",
                0.0,
            )
        )

        total_trades = int(
            result.get(
                "total_trades",
                result.get(
                    "trades",
                    0,
                ),
            )
        )

        max_drawdown = float(
            result.get(
                "max_drawdown",
                0.0,
            )
        )

        average_trade = float(
            result.get(
                "average_trade",
                0.0,
            )
        )

        trade_list = result.get(
            "trade_list",
            [],
        )

        if not isinstance(
            trade_list,
            list,
        ):

            trade_list = []

        # ----------------------------------------------------
        # A configuration is valid if it actually generated
        # at least one completed trade.
        # ----------------------------------------------------

        valid = (
            total_trades > 0
            and
            len(trade_list) > 0
        )

        # ----------------------------------------------------
        # Return normalised optimisation result
        # ----------------------------------------------------

        return {

            **configuration,

            "net_profit":
                net_profit,

            "profit":
                profit,

            "profit_factor":
                profit_factor,

            "win_rate":
                win_rate,

            "trade_count":
                total_trades,

            "total_trades":
                total_trades,

            "max_drawdown":
                max_drawdown,

            "average_trade":
                average_trade,

            "trade_list":
                trade_list,

            "valid":
                valid,

            "error":
                None,

            "result":
                result,

        }

    except Exception as error:

        # ----------------------------------------------------
        # Worker failure
        # ----------------------------------------------------

        return {

            **configuration,

            "ranking_score":
                -1000000.0,

            "net_profit":
                0.0,

            "profit":
                0.0,

            "profit_factor":
                0.0,

            "win_rate":
                0.0,

            "trade_count":
                0,

            "total_trades":
                0,

            "max_drawdown":
                999999.0,

            "average_trade":
                0.0,

            "trade_list":
                [],

            "valid":
                False,

            "error":
                f"{type(error).__name__}: "
                f"{error}",

            "result":
                None,

        }


# ============================================================
# BATCH WORKER
# ============================================================

def run_configuration_batch(
    configurations,
    dataframe,
    symbol,
    starting_cash,
    use_regime_filter=True,
):
    """
    Run a batch of configurations inside one worker.

    The dataframe is transferred to the worker once for the
    entire batch and then reused.
    """

    results = []

    for configuration in configurations:

        result = run_configuration(

            configuration=
                configuration,

            dataframe=
                dataframe,

            symbol=
                symbol,

            starting_cash=
                starting_cash,

            use_regime_filter=
                use_regime_filter,

        )

        results.append(
            result
        )

    return results


# ============================================================
# SPLIT CONFIGURATIONS
# ============================================================

def create_batches(
    configurations,
    workers,
):
    """
    Split configurations into approximately equal batches.
    """

    if not configurations:

        return []

    worker_count = min(
        max(
            1,
            workers,
        ),
        len(configurations),
    )

    batch_size = (
        len(configurations)
        +
        worker_count
        -
        1
    ) // worker_count

    batches = []

    for start in range(
        0,
        len(configurations),
        batch_size,
    ):

        batch = configurations[
            start:
            start + batch_size
        ]

        if batch:

            batches.append(
                batch
            )

    return batches


# ============================================================
# PARALLEL OPTIMIZER
# ============================================================

class ParallelOptimizer:

    def __init__(
        self,
        workers: int = 16,
        use_regime_filter: bool = True,
    ):

        self.workers = max(
            1,
            int(workers),
        )

        self.use_regime_filter = (
            use_regime_filter
        )

    # ========================================================
    # RUN
    # ========================================================

    def run(
        self,
        dataframe,
        symbol,
        starting_cash,
        configurations,
    ):
        """
        Run optimisation configurations in parallel.

        The current BacktestEngine interface is used directly.

        If dataframe is None, DatasetCache is used as a
        fallback.
        """

        # ----------------------------------------------------
        # LOAD DATASET FROM CACHE IF NECESSARY
        # ----------------------------------------------------

        if dataframe is None:

            print()

            print(
                f"Loading optimisation dataset "
                f"from cache: {symbol}"
            )

            dataframe = DatasetCache.get(

                symbol=
                    symbol,

                period=
                    "10y",

                interval=
                    "1d",

            )

        # ----------------------------------------------------
        # VALIDATE DATASET
        # ----------------------------------------------------

        if (
            dataframe is None
            or dataframe.empty
        ):

            print()

            print(
                "Optimisation aborted: "
                "dataset is empty."
            )

            return []

        # ----------------------------------------------------
        # VALIDATE CONFIGURATIONS
        # ----------------------------------------------------

        if not configurations:

            return []

        # ----------------------------------------------------
        # CREATE BATCHES
        # ----------------------------------------------------

        batches = create_batches(

            configurations,

            self.workers,

        )

        actual_workers = min(

            self.workers,

            len(batches),

        )

        print()

        print(
            f"Running "
            f"{len(configurations)} "
            f"tests using "
            f"{actual_workers} workers"
        )

        print(
            f"Configuration batches: "
            f"{len(batches)}"
        )

        print(
            f"Dataset candles: "
            f"{len(dataframe)}"
        )

        print()

        # ----------------------------------------------------
        # EXECUTE
        # ----------------------------------------------------

        results = []

        completed_batches = 0

        completed_tests = 0

        with ProcessPoolExecutor(
            max_workers=
                actual_workers
        ) as executor:

            futures = {}

            for batch_index, batch in enumerate(
                batches,
                start=1,
            ):

                future = executor.submit(

                    run_configuration_batch,

                    batch,

                    dataframe,

                    symbol,

                    starting_cash,

                    self.use_regime_filter,

                )

                futures[
                    future
                ] = (
                    batch_index,
                    len(batch),
                )

            # ------------------------------------------------
            # Collect completed workers
            # ------------------------------------------------

            for future in as_completed(
                futures
            ):

                batch_index, batch_size = (
                    futures[future]
                )

                try:

                    batch_results = (
                        future.result()
                    )

                except Exception as error:

                    batch_results = []

                    print()

                    print(
                        f"Worker batch "
                        f"{batch_index} "
                        f"failed: "
                        f"{type(error).__name__}: "
                        f"{error}"
                    )

                results.extend(
                    batch_results
                )

                completed_batches += 1

                completed_tests += (
                    batch_size
                )

                print(
                    f"Completed batch "
                    f"{completed_batches}/"
                    f"{len(batches)}"
                    f" "
                    f"({completed_tests}/"
                    f"{len(configurations)} "
                    f"tests)"
                )

        # ====================================================
        # OPTIMISATION DIAGNOSTICS
        # ====================================================

        valid_results = [

            result

            for result in results

            if result.get(
                "valid",
                False,
            )

        ]

        invalid_results = [

            result

            for result in results

            if not result.get(
                "valid",
                False,
            )

        ]

        print()

        print(
            "OPTIMISATION SUMMARY"
        )

        print(
            f"Valid trading configurations: "
            f"{len(valid_results)}"
        )

        print(
            f"Zero-trade / invalid configurations: "
            f"{len(invalid_results)}"
        )

        # ----------------------------------------------------
        # Show worker errors if any
        # ----------------------------------------------------

        errors = [

            result

            for result in results

            if result.get(
                "error"
            )

        ]

        if errors:

            print()

            print(
                f"Configurations with errors: "
                f"{len(errors)}"
            )

            first_error = errors[0].get(
                "error"
            )

            print(
                f"First optimiser error: "
                f"{first_error}"
            )

        # ----------------------------------------------------
        # No valid configurations
        # ----------------------------------------------------

        if not valid_results:

            print()

            print(
                "WARNING: NO VALID "
                "TRADING CONFIGURATION FOUND"
            )

            print(
                "Every optimisation configuration "
                "produced zero trades or failed."
            )

        return results