"""
Atlas AI Trading Platform 3.0

Backtesting Engine

Optimised configurable position lifecycle engine.

Supports:

- Long trades
- Short trades
- Dynamic score thresholds
- Dynamic confidence thresholds
- Dynamic ATR risk settings
- Cached datasets
- Fast optimisation runs
"""

from __future__ import annotations

import pandas as pd

from backtesting.historical_data import HistoricalData
from backtesting.strategy_runner import StrategyRunner
from backtesting.simulator import Simulator

from risk.risk_manager import create_trade



class BacktestEngine:


    # =====================================================
    # Shared dataset cache
    # =====================================================

    _data_cache: dict[str, pd.DataFrame] = {}



    def __init__(
        self,
        starting_cash: float = 100000.0,
    ):

        self.starting_cash = starting_cash

        self.data = HistoricalData()



    def _get_data(
        self,
        symbol: str,
    ) -> pd.DataFrame:


        if symbol in self._data_cache:

            return self._data_cache[symbol]



        dataframe = self.data.load(
            symbol
        )


        self._data_cache[symbol] = dataframe


        return dataframe



    def run(
        self,
        symbol: str | pd.DataFrame,
        score_threshold: int = 70,
        confidence_threshold: float = 0.70,
        atr_stop: float = 2.0,
        atr_target: float = 4.0,
    ):


        # =====================================================
        # Dataset handling
        # =====================================================

        if isinstance(
            symbol,
            pd.DataFrame,
        ):

            dataframe = symbol

            trade_symbol = "UNKNOWN"


        else:

            trade_symbol = symbol


            dataframe = self._get_data(
                symbol
            )



        # =====================================================
        # Strategy
        # =====================================================

        strategy = StrategyRunner(

            score_threshold=score_threshold,

            confidence_threshold=confidence_threshold,

        )



        signals = strategy.run(

            dataframe,

            trade_symbol,

        )



        # =====================================================
        # Simulator
        # =====================================================

        simulator = Simulator(

            self.starting_cash,

            atr_stop=atr_stop,

            atr_target=atr_target,

        )



        last_exit_index = -1



        # =====================================================
        # Trade lifecycle
        # =====================================================

        for item in signals:


            index = item["index"]



            if index <= last_exit_index:

                continue



            bias = item["bias"]



            if bias not in (

                "BUY",

                "SELL",

            ):

                continue



            if item["score"] < score_threshold:

                continue



            if item["confidence"] < confidence_threshold:

                continue



            window = dataframe.iloc[
                :index + 1
            ]



            direction = (

                "LONG"

                if bias == "BUY"

                else

                "SHORT"

            )



            trade = create_trade(

                trade_symbol,

                window,

                self.starting_cash,

                1.0,

                direction,

                item["confidence"]

            )



            if trade is None:

                continue



            simulated = simulator.simulate_trade(

                trade,

                dataframe,

                index

            )


            if simulated:

                last_exit_index = index



        return simulator.results()