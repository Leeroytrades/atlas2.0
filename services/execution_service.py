"""
Atlas AI Trading Platform

Execution Service
"""

from __future__ import annotations


class ExecutionService:

    def __init__(
        self,
        execution_manager,
        trade_repository,
        market_data,
    ):

        self.execution = execution_manager

        self.trades = trade_repository

        self.market = market_data

    def monitor(self):

        open_trades = self.trades.open_trades()

        prices = {}

        for trade in open_trades:

            df = self.market.get_history(
                trade.symbol
            )

            prices[
                trade.symbol
            ] = float(
                df["Close"].iloc[-1]
            )

        return self.execution.monitor_open_trades(
            open_trades,
            prices
        )