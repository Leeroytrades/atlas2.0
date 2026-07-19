"""
Atlas AI Trading Assistant 2.0

Trade Model
"""

from dataclasses import dataclass
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

    opened: datetime = datetime.now()