"""
Atlas AI Trading Platform 3.3

Strategy Router

Selects the correct strategy
based on detected market regime.
"""

from __future__ import annotations


from strategies.trend import TrendStrategy



class StrategyRouter:


    def __init__(self):

        self.strategies = [

            TrendStrategy(),

        ]



    def select(
        self,
        regime: str,
    ):


        for strategy in self.strategies:


            if strategy.enabled:

                if regime in strategy.regimes:

                    return strategy



        return None



    def info(self):

        return [

            strategy.info()

            for strategy in self.strategies

        ]