"""
Atlas Portfolio
"""

from __future__ import annotations

from dataclasses import dataclass, field

from risk.trade import Trade


@dataclass
class Portfolio:

    account_balance: float = 10000

    positions: list[Trade] = field(default_factory=list)

    def add_trade(self, trade: Trade):

        self.positions.append(trade)

    @property
    def total_positions(self):

        return len(self.positions)

    @property
    def exposure(self):

        return sum(
            trade.entry * trade.quantity
            for trade in self.positions
        )