"""
Atlas AI Trading Platform

Portfolio Model

Represents the trading account and all positions.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from models.trade import Trade


@dataclass(slots=True)
class Portfolio:
    """
    Trading account.
    """

    account_balance: float = 10000.00

    positions: list[Trade] = field(default_factory=list)

    closed_positions: list[Trade] = field(default_factory=list)

    account_name: str = "Primary"

    currency: str = "USD"

    @property
    def total_positions(self) -> int:
        """
        Number of open positions.
        """
        return len(self.positions)

    @property
    def total_closed(self) -> int:
        """
        Number of closed trades.
        """
        return len(self.closed_positions)

    @property
    def exposure(self) -> float:
        """
        Total capital currently at risk.
        """
        return round(

            sum(

                trade.risk_amount

                for trade in self.positions

                if trade.status == "OPEN"

            ),

            2

        )

    @property
    def equity(self) -> float:
        """
        Current account equity.
        """

        pnl = sum(

            trade.profit_loss

            for trade in self.closed_positions

        )

        return round(

            self.account_balance + pnl,

            2

        )

    @property
    def buying_power(self) -> float:
        """
        Available buying power.
        """

        return round(

            self.equity - self.exposure,

            2

        )

    def add_trade(
        self,
        trade: Trade
    ) -> None:
        """
        Add an open trade.
        """

        if any(

            t.symbol == trade.symbol
            and t.status == "OPEN"

            for t in self.positions

        ):

            return

        self.positions.append(
            trade
        )

    def close_trade(
        self,
        trade: Trade
    ) -> None:
        """
        Move a trade from open to closed.
        """

        if trade in self.positions:

            self.positions.remove(
                trade
            )

            self.closed_positions.append(
                trade
            )

    def has_position(
        self,
        symbol: str
    ) -> bool:
        """
        Check if a symbol is already open.
        """

        return any(

            trade.symbol == symbol
            and trade.status == "OPEN"

            for trade in self.positions

        )

    def get_position(
        self,
        symbol: str
    ) -> Trade | None:
        """
        Return an open position.
        """

        for trade in self.positions:

            if trade.symbol == symbol:

                return trade

        return None

    def clear(self) -> None:
        """
        Remove all positions.
        """

        self.positions.clear()

        self.closed_positions.clear()

    def summary(self) -> dict:
        """
        Portfolio summary.
        """

        return {

            "balance": self.account_balance,

            "equity": self.equity,

            "buying_power": self.buying_power,

            "open_positions": self.total_positions,

            "closed_positions": self.total_closed,

            "exposure": self.exposure,

        }

    def __str__(self) -> str:

        return (

            f"Portfolio("

            f"Balance={self.account_balance:.2f}, "

            f"Equity={self.equity:.2f}, "

            f"Open={self.total_positions})"

        )