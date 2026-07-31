"""
Atlas AI Trading Platform 3.0

Backtesting Service

Application bridge between:

Atlas Engine
        |
        v
Backtesting Engine
        |
        v
Analytics
"""

from __future__ import annotations


from backtesting.engine import BacktestEngine

from backtesting.analytics import MarketAnalytics



class BacktestingService:


    def __init__(self):

        pass



    # ==================================================
    # RUN SINGLE BACKTEST
    # ==================================================

    def run(
        self,
        symbol: str,
    ):

        engine = BacktestEngine()


        return engine.run(

            symbol

        )



    # ==================================================
    # RANK MARKETS
    # ==================================================

    def rank_markets(
        self,
        results: dict,
        count: int = 3,
    ):


        analytics = MarketAnalytics(

            results

        )


        return analytics.best_markets(

            count

        )