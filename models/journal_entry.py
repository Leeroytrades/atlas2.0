from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class JournalEntry:
    """
    Stores the reasoning and outcome behind an Atlas trade.
    """

    symbol: str
    direction: str

    entry_price: float
    exit_price: Optional[float]

    score: int
    confidence: float

    trend: str
    momentum: str
    volatility: str
    volume: str

    market_condition: str

    outcome: str = "OPEN"
    profit_loss: float = 0.0

    notes: str = ""

    created: datetime = datetime.now()

    @property
    def is_closed(self) -> bool:
        return self.outcome != "OPEN"

    @property
    def result(self) -> str:
        if self.profit_loss > 0:
            return "WIN"
        elif self.profit_loss < 0:
            return "LOSS"
        return "BREAKEVEN"