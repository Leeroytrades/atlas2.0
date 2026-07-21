"""
Atlas AI Trading Platform

Trade Model

This is the canonical Trade object used throughout Atlas.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class Trade:
    """
    Represents a single trade.
    """

    # Database ID
    id: Optional[int] = None

    # Instrument
    symbol: str = ""

    # LONG or SHORT
    direction: str = "LONG"

    # Prices
    entry: float = 0.0
    stop_loss: float = 0.0
    take_profit: float = 0.0

    # Position
    quantity: int = 0

    # Risk
    risk_amount: float = 0.0
    reward_amount: float = 0.0
    risk_reward: float = 0.0

    # Confidence
    confidence: float = 0.0

    # Lifecycle
    status: str = "OPEN"

    opened: datetime = field(
        default_factory=datetime.now
    )

    closed: Optional[datetime] = None

    # Results
    exit_price: Optional[float] = None

    profit_loss: float = 0.0

    # Notes
    notes: str = ""

    @property
    def is_open(self) -> bool:
        return self.status == "OPEN"

    @property
    def is_closed(self) -> bool:
        return self.status == "CLOSED"

    @property
    def duration(self):
        """
        Length of trade.
        """
        if self.closed is None:
            return datetime.now() - self.opened

        return self.closed - self.opened

    def close(
        self,
        exit_price: float
    ) -> None:
        """
        Close the trade and calculate P/L.
        """

        self.exit_price = exit_price

        self.closed = datetime.now()

        self.status = "CLOSED"

        if self.direction == "LONG":

            self.profit_loss = round(

                (exit_price - self.entry)
                * self.quantity,

                2

            )

        else:

            self.profit_loss = round(

                (self.entry - exit_price)
                * self.quantity,

                2

            )

    def to_dict(self) -> dict:
        """
        Convert trade to dictionary.
        """

        return {

            "id": self.id,

            "symbol": self.symbol,

            "direction": self.direction,

            "entry": self.entry,

            "stop_loss": self.stop_loss,

            "take_profit": self.take_profit,

            "quantity": self.quantity,

            "risk_amount": self.risk_amount,

            "reward_amount": self.reward_amount,

            "risk_reward": self.risk_reward,

            "confidence": self.confidence,

            "status": self.status,

            "opened": self.opened,

            "closed": self.closed,

            "exit_price": self.exit_price,

            "profit_loss": self.profit_loss,

            "notes": self.notes,

        }

    def __str__(self) -> str:

        return (

            f"{self.symbol} "

            f"{self.direction} "

            f"{self.status} "

            f"P/L: {self.profit_loss:.2f}"

        )