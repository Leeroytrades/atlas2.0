"""
Atlas AI Trading Platform 3.0

Execution Service

Monitors broker positions.

Responsibilities:

- Retrieve broker positions
- Check market prices
- Monitor stops/targets
- Trigger alerts
"""

from __future__ import annotations



class ExecutionService:


    def __init__(
        self,
        broker,
        trade_repository,
        market_data,
        alerts=None,
    ):

        self.broker = broker

        self.trades = trade_repository

        self.market = market_data

        self.alerts = alerts



    # ==================================================
    # MONITOR OPEN TRADES
    # ==================================================

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



        closed = self.broker.monitor_open_trades(

            open_trades,

            prices

        )



        if closed and self.alerts:


            for trade in closed:

                self.alerts.trade_closed(
                    trade
                )



        return closed