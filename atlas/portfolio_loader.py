"""
Atlas AI Trading Platform

Portfolio Loader

Loads saved open trades from SQLite
into the active session portfolio.
"""

from __future__ import annotations



class PortfolioLoader:


    def __init__(
        self,
        trade_repository
    ):

        self.trades = trade_repository



    def load(
        self,
        portfolio
    ):

        """
        Restore open trades from database.
        """


        open_trades = self.trades.open_trades()



        for trade in open_trades:


            exists = False


            for position in portfolio.positions:


                if position.symbol == trade.symbol:

                    exists = True

                    break



            if exists:

                continue



            portfolio.add_trade(

                trade

            )


        return portfolio