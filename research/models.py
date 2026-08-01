"""
Atlas Research Models
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

import pandas as pd


@dataclass(slots=True, frozen=True)
class PreparedDataset:
    """
    Immutable research dataset.

    Contains a fully prepared DataFrame together
    with the metadata required for optimisation.
    """

    symbol: str

    period: str

    interval: str

    dataframe: pd.DataFrame

    indicator_version: str = "1.0"

    score_version: str = "1.0"

    created: datetime = field(
        default_factory=datetime.utcnow,
    )

    @property
    def rows(self) -> int:
        return len(self.dataframe)

    @property
    def columns(self) -> int:
        return len(self.dataframe.columns)