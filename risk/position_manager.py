"""
Atlas AI Trading Platform

Position Manager

Responsible for position validation.
"""

from __future__ import annotations

from models.trade import Trade


class PositionManager:

    def __init__(
        self,
        trade_repository,
    ):

        self.trades = trade_repository

    def open_positions(self) -> list[Trade]:
        """
        Return all open trades.
        """

        return self.trades.open_trades()

    def has_open_position(
        self,
        symbol: str,
    ) -> bool:
        """
        Check if a symbol already has an open trade.
        """

        return any(

            trade.symbol == symbol

            for trade in self.open_positions()

        )

    def can_open_position(
        self,
        symbol: str,
    ) -> bool:
        """
        Can Atlas open another trade?
        """

        return not self.has_open_position(
            symbol
        )

    def open_position_count(
        self,
    ) -> int:

        return len(
            self.open_positions()
        )

    def symbols_open(
        self,
    ) -> list[str]:

        return [

            trade.symbol

            for trade in self.open_positions()

        ]