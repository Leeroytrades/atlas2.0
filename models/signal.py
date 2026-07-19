"""
Atlas AI Trading Assistant 2.0

Trading Signal Model
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class SignalType(Enum):
    """Trading signal types."""

    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class SignalStrength(Enum):
    """Signal confidence."""

    WEAK = "WEAK"
    MODERATE = "MODERATE"
    STRONG = "STRONG"


@dataclass(slots=True)
class Signal:
    """
    Represents a complete trading signal.
    """

    symbol: str

    signal: SignalType

    score: int

    confidence: float

    strength: SignalStrength

    entry_price: float

    stop_loss: Optional[float] = None

    take_profit: Optional[float] = None

    quantity: float = 0.0

    timestamp: datetime = field(default_factory=datetime.utcnow)

    notes: str = ""

    @property
    def tradeable(self) -> bool:
        """
        Returns True if BUY or SELL.
        """
        return self.signal != SignalType.HOLD

    @property
    def risk(self) -> Optional[float]:
        if self.stop_loss is None:
            return None

        return abs(self.entry_price - self.stop_loss)

    @property
    def reward(self) -> Optional[float]:
        if self.take_profit is None:
            return None

        return abs(self.take_profit - self.entry_price)

    @property
    def risk_reward_ratio(self) -> Optional[float]:

        risk = self.risk
        reward = self.reward

        if risk is None:
            return None

        if reward is None:
            return None

        if risk == 0:
            return None

        return reward / risk

    def __str__(self) -> str:

        return (
            f"{self.symbol} | "
            f"{self.signal.value} | "
            f"Score={self.score} | "
            f"Confidence={self.confidence:.1%}"
        )