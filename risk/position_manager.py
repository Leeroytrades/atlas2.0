"""
Atlas AI Trading Assistant 2.4

Position Manager

Responsible for:

- Open position tracking
- Duplicate prevention
- Position limits
- Risk limits
- Portfolio protection
"""

from __future__ import annotations

from models.trade import Trade


class PositionManager:


    def __init__(
        self,
        trade_repository,
        max_positions: int = 5,
        max_risk_percent: float = 5.0,
        account_size: float = 10000.0,
    ):

        self.trades = trade_repository

        self.max_positions = max_positions

        self.max_risk_percent = max_risk_percent

        self.account_size = account_size



    # =====================================================
    # OPEN POSITIONS
    # =====================================================

    def open_positions(self) -> list[Trade]:
        """
        Return all active trades.
        """

        return self.trades.open_trades()



    # =====================================================
    # POSITION CHECKS
    # =====================================================

    def has_open_position(
        self,
        symbol: str,
    ) -> bool:
        """
        Check if symbol already exists.
        """

        return any(

            trade.symbol == symbol

            for trade in self.open_positions()

        )



    def open_position_count(
        self,
    ) -> int:
        """
        Number of active positions.
        """

        return len(

            self.open_positions()

        )



    def total_risk(
        self,
    ) -> float:
        """
        Current open trade risk.
        """

        return sum(

            getattr(

                trade,

                "risk_amount",

                0

            )

            for trade in self.open_positions()

        )



    # =====================================================
    # CAN OPEN POSITION
    # =====================================================

    def can_open_position(
        self,
        symbol: str,
        additional_risk: float = 0.0,
    ) -> bool:
        """
        Full risk validation.
        """


        # Duplicate symbol check

        if self.has_open_position(symbol):

            return False



        # Maximum positions

        if self.open_position_count() >= self.max_positions:

            return False



        # Maximum account risk

        max_risk_amount = (

            self.account_size

            *

            (self.max_risk_percent / 100)

        )


        projected_risk = (

            self.total_risk()

            +

            additional_risk

        )


        if projected_risk > max_risk_amount:

            return False



        return True



    # =====================================================
    # INFORMATION
    # =====================================================

    def symbols_open(
        self,
    ) -> list[str]:
        """
        Return active symbols.
        """

        return [

            trade.symbol

            for trade in self.open_positions()

        ]



    def exposure(
        self,
    ) -> float:
        """
        Total capital exposed.
        """

        return sum(

            trade.entry * trade.quantity

            for trade in self.open_positions()

        )



    def summary(
        self,
    ) -> dict:
        """
        Position overview.
        """

        return {

            "positions":

                self.open_position_count(),


            "max_positions":

                self.max_positions,


            "symbols":

                self.symbols_open(),


            "exposure":

                round(

                    self.exposure(),

                    2

                ),


            "risk":

                round(

                    self.total_risk(),

                    2

                ),


        }