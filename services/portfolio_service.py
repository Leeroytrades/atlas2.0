"""
Atlas AI Trading Platform

Portfolio Service

Handles portfolio operations.
"""

from __future__ import annotations


class PortfolioService:

    def __init__(
        self,
        portfolio,
        repository,
    ):

        self.portfolio = portfolio

        self.repository = repository

    def add_trade(
        self,
        trade,
    ):

        self.portfolio.add_trade(
            trade
        )

        self.repository.save(
            self.portfolio
        )

    def close_trade(
        self,
        trade,
    ):

        self.portfolio.close_trade(
            trade
        )

        self.repository.save(
            self.portfolio
        )

    def has_position(
        self,
        symbol: str,
    ):

        return self.portfolio.has_position(
            symbol
        )

    def summary(self):

        return self.portfolio.summary()