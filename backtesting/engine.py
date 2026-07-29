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
        starting_cash: float = 100000.0,
        minimum_score: int = 70,
        minimum_confidence: float = 0.70
    ):


        self.starting_cash = starting_cash

        self.minimum_score = minimum_score

        self.minimum_confidence = minimum_confidence


        self.data = HistoricalData()

        self.strategy = StrategyRunner()

        self.simulator = Simulator(

            starting_cash

        )



    def get_close(
        self,
        dataframe,
        index
    ):

        """
        Extract close price from dataframe.
        Handles yfinance formats.
        """


        row = dataframe.iloc[index]


        if "Close" in row:

            return float(
                row["Close"]
            )


        if ("Close",) in row.index:

            return float(
                row[("Close",)]
            )


        for column in row.index:

            if isinstance(column, tuple):

                if column[0] == "Close":

                    return float(
                        row[column]
                    )


        raise ValueError(
            "Close price not found"
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


        for item in signals:


            index = item["index"]


            score = item["score"]

            confidence = item["confidence"]

            bias = item["bias"]



            if score < self.minimum_score:

                continue


            if confidence < self.minimum_confidence:

                continue


            if bias != "BUY":

                continue



            try:


                entry = self.get_close(

                    dataframe,

                    index

                )


                future = self.get_close(

                    dataframe,

                    index + 5

                )


            except Exception as error:

                print(
                    "Price error:",
                    error
                )

                continue



            self.simulator.execute(

                symbol,

                entry,

                "LONG",

                future

            )



        report = BacktestReport(

            self.simulator.trades,

            self.starting_cash

        )


        return report.generate()