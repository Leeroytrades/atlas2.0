"""
Atlas AI Trading Platform

Paper Broker

Simulated execution environment.
"""

from __future__ import annotations

from brokers.base import Broker


class PaperBroker(Broker):
    """
    Paper trading broker.
    """


    def __init__(
        self,
        trade_repository,
    ):

        self.trades = trade_repository



    def submit_order(
        self,
        trade,
    ):

        self.trades.save(
            trade
        )

        return trade



    def close_order(
        self,
        trade,
        exit_price: float,
    ):

        self.trades.close_trade(
            trade,
            exit_price,
        )

        return trade



    def get_positions(self):

        return self.trades.open_trades()



    def get_account(self):

        return {

            "type": "PAPER",

            "positions": len(
                self.get_positions()
            )

        }