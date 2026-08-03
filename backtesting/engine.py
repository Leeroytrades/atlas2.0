"""
Atlas AI Trading Platform 3.3

Backtesting Engine

Supports:

- Long trades
- Short trades
- Dynamic parameters
- Optional regime filtering
- Strategy routing
- Indicator generation
"""

from __future__ import annotations


import pandas as pd


from backtesting.historical_data import HistoricalData

from backtesting.strategy_runner import StrategyRunner

from backtesting.simulator import Simulator


from risk.risk_manager import create_trade


from strategy.regime_filter import RegimeFilter


from indicators.composite import build_indicator_set



class BacktestEngine:


    _data_cache: dict[str, pd.DataFrame] = {}



    def __init__(

        self,

        starting_cash: float = 100000.0,

        use_regime_filter: bool = False,

    ):


        self.starting_cash = starting_cash

        self.use_regime_filter = use_regime_filter


        self.data = HistoricalData()


        self.regime_filter = RegimeFilter()



        print()

        print(

            f"REGIME FILTER ACTIVE: {self.use_regime_filter}"

        )

        print()



    # =====================================================
    # Data Loading
    # =====================================================

    def _get_data(

        self,

        symbol: str,

    ):


        if symbol in self._data_cache:


            return self._data_cache[symbol]



        dataframe = self.data.load(

            symbol

        )


        # ---------------------------------
        # Add indicators
        # ---------------------------------

        dataframe = build_indicator_set(

            dataframe

        )



        self._data_cache[symbol] = dataframe



        return dataframe




    # =====================================================
    # Backtest Runner
    # =====================================================

    def run(

        self,

        symbol: str | pd.DataFrame,

        score_threshold: int = 70,

        confidence_threshold: float = 0.70,

        atr_stop: float = 2.0,

        atr_target: float = 4.0,

    ):



        if isinstance(symbol, pd.DataFrame):


            dataframe = symbol


            trade_symbol = "UNKNOWN"



            dataframe = build_indicator_set(

                dataframe

            )



        else:


            trade_symbol = symbol


            dataframe = self._get_data(

                symbol

            )



        strategy = StrategyRunner(

            score_threshold=score_threshold,

            confidence_threshold=confidence_threshold,

        )



        signals = strategy.run(

            dataframe,

            trade_symbol,

        )



        simulator = Simulator(

            self.starting_cash,

            atr_stop=atr_stop,

            atr_target=atr_target,

        )



        last_exit_index = -1



        for item in signals:


            index = item["index"]



            if index <= last_exit_index:

                continue



            bias = item["bias"]



            if bias not in (

                "BUY",

                "SELL"

            ):

                continue



            if item["score"] < score_threshold:

                continue



            if item["confidence"] < confidence_threshold:

                continue




            window = dataframe.iloc[:index + 1]



            # ---------------------------------
            # Regime Filter
            # ---------------------------------

            if self.use_regime_filter:


                allowed = self.regime_filter.is_allowed(

                    window

                )


                if not allowed:

                    continue




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

                item["confidence"],

            )




            if trade is None:

                continue




            simulated = simulator.simulate_trade(

                trade,

                dataframe,

                index,

            )



            if simulated:


                last_exit_index = index




        return simulator.results()
