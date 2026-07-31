"""
Atlas AI Trading Platform 3.0

Backtesting Engine

Configurable position lifecycle engine.

Supports:

- Dynamic score thresholds
- Dynamic confidence thresholds
- Dynamic ATR risk settings
- Historical strategy testing
"""

from __future__ import annotations


from backtesting.historical_data import HistoricalData

from backtesting.strategy_runner import StrategyRunner

from backtesting.simulator import Simulator

from risk.risk_manager import create_trade





class BacktestEngine:


    def __init__(
        self,
        starting_cash: float = 100000.0,
    ):


        self.starting_cash = starting_cash


        self.data = HistoricalData()



    def run(
        self,
        symbol: str,
        score_threshold: int = 70,
        confidence_threshold: float = 0.70,
        atr_stop: float = 2.0,
        atr_target: float = 4.0,
    ):


        dataframe = self.data.load(

            symbol

        )


        strategy = StrategyRunner(

            score_threshold=score_threshold,

            confidence_threshold=confidence_threshold,

        )


        simulator = Simulator(

            self.starting_cash,

            atr_stop=atr_stop,

            atr_target=atr_target,

        )



        signals = strategy.run(

            dataframe,

            symbol

        )



        last_exit_index = -1



        for item in signals:



            index = item["index"]



            if index <= last_exit_index:

                continue



            if item["bias"] != "BUY":

                continue



            if item["score"] < score_threshold:

                continue



            if item["confidence"] < confidence_threshold:

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



            simulated = simulator.simulate_trade(

                trade,

                dataframe,

                index

            )



            if simulated:

                last_exit_index = index



        return simulator.results()