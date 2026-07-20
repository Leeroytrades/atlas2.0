"""
Atlas AI Trading Assistant 2.0

Trade Model
"""

from __future__ import annotations

from dataclasses import dataclass, field

from datetime import datetime



@dataclass(slots=True)
class Trade:

    symbol: str

    direction: str

    entry: float

    stop_loss: float

    take_profit: float

    quantity: int

    risk_amount: float

    reward_amount: float

    risk_reward: float

    confidence: float


    id: int | None = None

    status: str = "OPEN"

    opened: datetime = field(
        default_factory=datetime.now
    )

    closed: datetime | None = None

    exit_price: float | None = None

    profit_loss: float | None = None