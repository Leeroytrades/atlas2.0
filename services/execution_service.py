"""
Atlas AI Trading Platform 3.0

Execution Service

Monitors broker positions.
"""

from __future__ import annotations



class ExecutionService:


    def __init__(
        self,
        broker,
        trade_repository,
        market_data,
    ):

        self.broker = broker

        self.trades = trade_repository

        self.market = market_data



    def monitor(self):


        open_trades = self.broker.get_positions()


        prices = {}



        for trade in open_trades:


            df = self.market.get_history(

                trade.symbol

            )


            prices[trade.symbol] = float(

                df["Close"].iloc[-1]

            )



        return self.broker.monitor_open_trades(

            open_trades,

            prices

        )