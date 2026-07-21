"""
Atlas AI Trading Platform

Strategy Service

Creates scorecards from market data.
"""

from __future__ import annotations

from data.market_data import MarketData

from indicators.composite import build_indicator_set

from strategy.signal_generator import generate_scorecard


class StrategyService:

    def __init__(self):

        self.market = MarketData()

    def analyse(
        self,
        symbol: str,
    ):

        df = self.market.get_history(
            symbol
        )

        df = build_indicator_set(
            df
        )

        score = generate_scorecard(
            df
        )

        return score, df