"""
Atlas AI Trading Platform 4.4

Multi Market Backtesting Engine

Runs Atlas backtests across multiple symbols.

Supports:

    MultiBacktestEngine(
        starting_cash=100000
    ).run(
        symbols,
        dataframes
    )

where dataframes is:

    {
        "SPY": spy_dataframe,
        "QQQ": qqq_dataframe,
        "AAPL": aapl_dataframe,
    }

A callable data provider is also supported:

    engine.run(
        symbols,
        data_provider=load_data
    )

The BacktestEngine remains the canonical engine for each
individual market.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping

from backtesting.engine import BacktestEngine


class MultiBacktestEngine:

    def __init__(
        self,
        starting_cash: float = 100000.0,
        minimum_score: int = 70,
        minimum_confidence: float = 0.70,
        atr_stop: float = 2.0,
        atr_target: float = 4.0,
        commission: float = 1.0,
        slippage: float = 0.01,
        max_hold: int = 100,
        breakeven_atr: float = 1.5,
    ):

        self.starting_cash = float(
            starting_cash
        )

        self.minimum_score = int(
            minimum_score
        )

        self.minimum_confidence = float(
            minimum_confidence
        )

        self.atr_stop = float(
            atr_stop
        )

        self.atr_target = float(
            atr_target
        )

        self.commission = float(
            commission
        )

        self.slippage = float(
            slippage
        )

        self.max_hold = max(
            1,
            int(max_hold),
        )

        self.breakeven_atr = max(
            0.0,
            float(breakeven_atr),
        )

    # ========================================================
    # CREATE ENGINE
    # ========================================================

    def _create_engine(self):

        return BacktestEngine(

            starting_cash=
                self.starting_cash,

            minimum_score=
                self.minimum_score,

            minimum_confidence=
                self.minimum_confidence,

            atr_stop=
                self.atr_stop,

            atr_target=
                self.atr_target,

            commission=
                self.commission,

            slippage=
                self.slippage,

            max_hold=
                self.max_hold,

            breakeven_atr=
                self.breakeven_atr,
        )

    # ========================================================
    # RUN MULTIPLE MARKETS
    # ========================================================

    def run(
        self,
        symbols: list[str],
        dataframes: Mapping | None = None,
        data_provider: Callable | None = None,
    ):
        """
        Run a backtest for every supplied symbol.

        Parameters
        ----------
        symbols:
            List of symbols.

        dataframes:
            Mapping of symbol -> historical dataframe.

        data_provider:
            Optional callable accepting a symbol and returning
            its historical dataframe.

        Examples
        --------

        results = engine.run(
            ["SPY", "QQQ"],
            dataframes={
                "SPY": spy_df,
                "QQQ": qqq_df,
            },
        )

        Or:

        results = engine.run(
            ["SPY", "QQQ"],
            data_provider=load_market_data,
        )
        """

        if not symbols:

            return {}

        if (
            dataframes is None
            and data_provider is None
        ):

            raise ValueError(
                "MultiBacktestEngine.run() requires either "
                "dataframes or data_provider."
            )

        results = {}

        # ====================================================
        # SYMBOL LOOP
        # ====================================================

        for symbol in symbols:

            print()
            print(
                f"Running backtest: {symbol}"
            )

            # ------------------------------------------------
            # GET DATAFRAME
            # ------------------------------------------------

            dataframe = None

            try:

                if data_provider is not None:

                    dataframe = data_provider(
                        symbol
                    )

                else:

                    dataframe = dataframes.get(
                        symbol
                    )

            except Exception as error:

                print(
                    f"Failed loading data for "
                    f"{symbol}: {error}"
                )

                continue

            # ------------------------------------------------
            # DATA VALIDATION
            # ------------------------------------------------

            if dataframe is None:

                print(
                    f"Failed {symbol}: "
                    "No historical dataframe supplied."
                )

                continue

            # ------------------------------------------------
            # RUN INDIVIDUAL BACKTEST
            # ------------------------------------------------

            engine = self._create_engine()

            try:

                result = engine.run(
                    symbol=symbol,
                    dataframe=dataframe,
                )

                results[symbol] = result

            except Exception as error:

                print(
                    f"Failed {symbol}: {error}"
                )

        # ====================================================
        # SUMMARY
        # ====================================================

        print()
        print(
            "MULTI-MARKET BACKTEST COMPLETE"
        )
        print(
            f"Markets requested: {len(symbols)}"
        )
        print(
            f"Markets completed: {len(results)}"
        )

        return results