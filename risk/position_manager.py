"""
Atlas AI Trading Platform 3.0

Position Manager

Controls:

- Position limits
- Risk validation
- Exposure checks
- Account risk
"""

from __future__ import annotations


from core.config import Config





class PositionManager:


    def __init__(
        self,
        trade_repository,
    ):

        self.trades = trade_repository



    # ==================================================
    # OPEN POSITIONS
    # ==================================================

    def open_positions(self):

        return self.trades.open_trades()



    # ==================================================
    # CHECK EXISTING POSITION
    # ==================================================

    def has_open_position(
        self,
        symbol: str,
    ):


        positions = self.open_positions()



        for trade in positions:

            if trade.symbol == symbol:

                return True



        return False



    # ==================================================
    # RISK LIMIT CHECK
    # ==================================================

    def can_open_position(
        self,
        symbol: str,
        risk_amount: float,
    ):



        max_risk = (

            Config.ACCOUNT_SIZE

            *

            Config.RISK_PERCENT

            /

            100

        )



        if risk_amount > max_risk:

            return False



        return True



    # ==================================================
    # CURRENT EXPOSURE
    # ==================================================

    def exposure(self):


        total = 0



        for trade in self.open_positions():


            total += (

                trade.entry

                *

                trade.quantity

            )



        return total



    # ==================================================
    # RISK USED
    # ==================================================

    def risk_used(self):


        total = 0



        for trade in self.open_positions():


            total += trade.risk_amount



        return total



    # ==================================================
    # AVAILABLE RISK
    # ==================================================

    def available_risk(self):


        allowed = (

            Config.ACCOUNT_SIZE

            *

            Config.RISK_PERCENT

            /

            100

        )



        return max(

            allowed - self.risk_used(),

            0

        )