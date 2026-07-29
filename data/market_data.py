"""
Market data access layer.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
import yfinance as yf


class MarketData:

    def __init__(self, cache_directory: str = "data"):

        self.cache_directory = Path(cache_directory)

    # ---------------------------------------------------------
    # Download history
    # ---------------------------------------------------------

    def get_history(
        self,
        symbol: str,
        period: str = "2y",
        interval: str = "1d",
    ) -> pd.DataFrame:

        df = yf.download(
            symbol,
            period=period,
            interval=interval,
            auto_adjust=True,
            progress=False,
        )

        if df.empty:
            raise ValueError(f"No data returned for {symbol}")

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df[["Open", "High", "Low", "Close", "Volume"]]

        for col in df.columns:

            if isinstance(df[col], pd.DataFrame):
                df[col] = df[col].iloc[:, 0]

        return df

    # ---------------------------------------------------------
    # Latest Market Price
    # ---------------------------------------------------------

    def get_price(
        self,
        symbol: str,
    ) -> float:
        """
        Returns the latest closing price.
        """

        df = self.get_history(
            symbol,
            period="5d",
            interval="1d",
        )

        return float(df["Close"].iloc[-1])

    # ---------------------------------------------------------
    # Cache
    # ---------------------------------------------------------

    def save_csv(
        self,
        df: pd.DataFrame,
        symbol: str,
    ) -> Path:

        self.cache_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        path = self.cache_directory / f"{symbol}.csv"

        df.to_csv(path)

        return path

    def load_csv(
        self,
        symbol: str,
    ) -> Optional[pd.DataFrame]:

        path = self.cache_directory / f"{symbol}.csv"

        if not path.exists():
            return None

        return pd.read_csv(
            path,
            index_col=0,
            parse_dates=True,
        )