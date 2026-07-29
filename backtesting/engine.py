"""
Atlas AI Trading Assistant 2.3

Backtesting Engine

Controls:

- Historical data loading
- Strategy execution
- Trade simulation
- Performance reporting
"""

from __future__ import annotations


from backtesting.historical_data import HistoricalData

from backtesting.strategy_runner import StrategyRunner

from backtesting.simulator import Simulator

from backtesting.reports import BacktestReport



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

        """
        Run complete Atlas backtest.
        """


        dataframe = self.data.load(

            symbol

        )


        signals = self.strategy.run(

            dataframe,

            symbol

        )


        self.simulator.run(

            symbol,

            dataframe,

            signals

        )


        report = BacktestReport(

            self.simulator.trades,

            self.starting_cash

        )


        return report.generate()