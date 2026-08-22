"""
Atlas AI Trading Platform 4.2

Trade Model

This is the canonical Trade object used throughout Atlas.

The Trade model carries the complete lifecycle state of a
simulated or live trade, including strategy attribution.
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

    # =========================================================
    # DATABASE ID
    # =========================================================

    id: Optional[int] = None

    # =========================================================
    # INSTRUMENT
    # =========================================================

    symbol: str = ""

    # =========================================================
    # DIRECTION
    # =========================================================

    # LONG or SHORT
    direction: str = "LONG"

    # =========================================================
    # PRICES
    # =========================================================

    entry: float = 0.0

    stop_loss: float = 0.0

    take_profit: float = 0.0

    # =========================================================
    # POSITION
    # =========================================================

    quantity: int = 0

    # =========================================================
    # RISK
    # =========================================================

    risk_amount: float = 0.0

    reward_amount: float = 0.0

    risk_reward: float = 0.0

    # =========================================================
    # CONFIDENCE
    # =========================================================

    confidence: float = 0.0

    # =========================================================
    # STRATEGY ATTRIBUTION
    # =========================================================

    # Actual strategy responsible for generating the trade.
    #
    # Examples:
    #
    #   TrendStrategy
    #   RangeStrategy
    #   VolatilityStrategy
    #
    # This field is intentionally part of the canonical Trade
    # object because the backtester needs to preserve strategy
    # attribution from signal generation through to diagnostics.
    strategy: str = "UNKNOWN"

    # =========================================================
    # LIFECYCLE
    # =========================================================

    status: str = "OPEN"

    opened: datetime = field(
        default_factory=datetime.now
    )

    closed: Optional[datetime] = None

    # =========================================================
    # RESULTS
    # =========================================================

    exit_price: Optional[float] = None

    profit_loss: float = 0.0

    # =========================================================
    # NOTES
    # =========================================================

    notes: str = ""

    # =========================================================
    # STATUS PROPERTIES
    # =========================================================

    @property
    def is_open(self) -> bool:
        """
        Return True when the trade is currently open.
        """

        return self.status == "OPEN"

    @property
    def is_closed(self) -> bool:
        """
        Return True when the trade is closed.
        """

        return self.status == "CLOSED"

    # =========================================================
    # DURATION
    # =========================================================

    @property
    def duration(self):
        """
        Return the duration of the trade.
        """

        if self.closed is None:

            return (
                datetime.now()
                -
                self.opened
            )

        return (
            self.closed
            -
            self.opened
        )

    # =========================================================
    # CLOSE TRADE
    # =========================================================

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

                (
                    exit_price
                    -
                    self.entry
                )
                *
                self.quantity,

                2
            )

        else:

            self.profit_loss = round(

                (
                    self.entry
                    -
                    exit_price
                )
                *
                self.quantity,

                2
            )

    # =========================================================
    # SERIALISATION
    # =========================================================

    def to_dict(self) -> dict:
        """
        Convert the trade to a dictionary.

        Strategy attribution is included so that database
        persistence and research diagnostics retain the
        originating strategy.
        """

        return {

            "id":
                self.id,

            "symbol":
                self.symbol,

            "direction":
                self.direction,

            "entry":
                self.entry,

            "stop_loss":
                self.stop_loss,

            "take_profit":
                self.take_profit,

            "quantity":
                self.quantity,

            "risk_amount":
                self.risk_amount,

            "reward_amount":
                self.reward_amount,

            "risk_reward":
                self.risk_reward,

            "confidence":
                self.confidence,

            "strategy":
                self.strategy,

            "status":
                self.status,

            "opened":
                self.opened,

            "closed":
                self.closed,

            "exit_price":
                self.exit_price,

            "profit_loss":
                self.profit_loss,

            "notes":
                self.notes,
        }

    # =========================================================
    # STRING REPRESENTATION
    # =========================================================

    def __str__(self) -> str:

        return (

            f"{self.symbol} "

            f"{self.direction} "

            f"{self.status} "

            f"{self.strategy} "

            f"P/L: "
            f"{self.profit_loss:.2f}"

        )