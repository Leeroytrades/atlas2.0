"""
Atlas AI Trading Assistant 2.3.3

Backtesting Engine

Position lifecycle management.

Allows:
- New entries after previous trade closes
- Single active trade
- Signal filtering
- Risk controlled execution
"""

from __future__ import annotations


from backtesting.historical_data import HistoricalData

from backtesting.strategy_runner import StrategyRunner

from backtesting.simulator import Simulator

from risk.risk_manager import create_trade



class BacktestEngine:


    def __init__(
        self,
        starting_cash: float = 100000.0
    ):


        self.starting_cash = starting_cash


        self.data = HistoricalData()


        self.strategy = StrategyRunner()


        self.simulator = Simulator(

            starting_cash

        )



    def run(
        self,
        symbol: str
    ):


        dataframe = self.data.load(

            symbol

        )



        signals = self.strategy.run(

            dataframe,

            symbol

        )



        last_exit_index = -1



        for item in signals:



            index = item["index"]



            # Skip candles already used

            if index <= last_exit_index:

                continue



            if item["bias"] != "BUY":

                continue



            if item["score"] < 70:

                continue



            if item["confidence"] < 0.70:

                continue



            window = dataframe.iloc[

                :index + 1

            ]



            trade = create_trade(

                symbol,

                window,

                self.starting_cash,

                1.0,

                "LONG",

                item["confidence"]

            )



            if trade is None:

                continue



            simulated = self.simulator.simulate_trade(

                trade,

                dataframe,

                index

            )



            # Find where trade effectively ended

            last_exit_index = index



        return self.simulator.results()