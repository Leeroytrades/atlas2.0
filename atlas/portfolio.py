"""
Atlas AI Trading Assistant 2.0

Portfolio Model
"""

from __future__ import annotations

from dataclasses import dataclass, field



@dataclass
class Portfolio:

    account_balance: float = 10000

    positions: list = field(
        default_factory=list
    )


    def add_trade(
        self,
        trade
    ):

        self.positions.append(
            trade
        )


    @property
    def total_positions(self):

        return len(
            self.positions
        )


    @property
    def exposure(self):

        return sum(
            trade.entry * trade.quantity
            for trade in self.positions
        )


    @property
    def total_risk(self):

        return sum(
            getattr(
                trade,
                "risk_amount",
                0
            )
            for trade in self.positions
        )


    @property
    def available_balance(self):

        return (
            self.account_balance
            -
            self.exposure
        )


    @property
    def unrealized_profit_loss(self):

        return sum(
            getattr(
                trade,
                "profit_loss",
                0
            ) or 0

            for trade in self.positions
        )


    def summary(self):

        return {

            "Account Balance":
                self.account_balance,

            "Open Positions":
                self.total_positions,

            "Exposure":
                self.exposure,

            "Risk":
                self.total_risk,

            "Available":
                self.available_balance,

            "Unrealized P/L":
                self.unrealized_profit_loss,

        }