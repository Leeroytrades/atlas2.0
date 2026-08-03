"""
Atlas AI Trading Platform 4.0

Strategy Registry

Manages all available
Atlas trading strategies.
"""

from __future__ import annotations


from strategies.base import BaseStrategy

from strategies.trend import TrendStrategy



class StrategyRegistry:


    def __init__(self):

        self.strategies: dict[str, BaseStrategy] = {}


        self.load_default_strategies()



    # =====================================================
    # Load Built-in Strategies
    # =====================================================

    def load_default_strategies(
        self,
    ):

        self.register(

            TrendStrategy()

        )



    # =====================================================
    # Register Strategy
    # =====================================================

    def register(
        self,
        strategy: BaseStrategy,
    ):


        self.strategies[

            strategy.name

        ] = strategy



    # =====================================================
    # Get Strategy
    # =====================================================

    def get(
        self,
        name: str,
    ):


        return self.strategies.get(

            name

        )



    # =====================================================
    # All Strategies
    # =====================================================

    def all(
        self,
    ):


        return list(

            self.strategies.values()

        )



    # =====================================================
    # Regime Filtering
    # =====================================================

    def available_for_regime(
        self,
        regime: str,
    ):


        return [

            strategy

            for strategy

            in self.strategies.values()

            if strategy.enabled

            and strategy.supports_regime(

                regime

            )

        ]