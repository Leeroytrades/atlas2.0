"""
Atlas AI Trading Assistant 2.0

Position Manager

Controls:
- Duplicate position prevention
- Symbol exposure checks
- Open position validation
"""

from __future__ import annotations



class PositionManager:


    def __init__(
        self,
        trade_repository
    ):

        self.trades = trade_repository



    def has_open_position(
        self,
        symbol: str
    ):

        open_trades = self.trades.open_trades()


        for trade in open_trades:

            if trade.symbol == symbol:

                return True


        return False



    def can_open_position(
        self,
        symbol: str
    ):

        return not self.has_open_position(
            symbol
        )



    def open_position_count(
        self
    ):

        return len(
            self.trades.open_trades()
        )



    def symbols_open(
        self
    ):

        return [

            trade.symbol

            for trade in self.trades.open_trades()

        ]