"""
Atlas AI Trading Assistant 2.0

Database Models
"""

from __future__ import annotations

from dataclasses import dataclass

from datetime import datetime



@dataclass
class TradeRecord:

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

    opened: datetime

    status: str

    closed: datetime | None

    exit_price: float | None

    profit_loss: float | None