"""
Market data access layer.
"""

from __future__ import annotations

import pandas as pd
import yfinance as yf

from cache import CacheManager
from config.settings import settings


class MarketData:
    """Provides historical and latest market data."""

    def __init__(self) -> None:

        self.cache = CacheManager()

    # ------------------------------------------------------------------
    # Download Data
    # ------------------------------------------------------------------

    def _download(
        self,
        symbol: str,
        period: str,
        interval: str,
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

        df = df[["Open", "High", "Low", "Close", "Volume"]].copy()

        for column in df.columns:

            if isinstance(df[column], pd.DataFrame):
                df[column] = df[column].iloc[:, 0]

        df.sort_index(inplace=True)

        return df

    # ------------------------------------------------------------------
    # Historical Data
    # ------------------------------------------------------------------

    def get_history(
        self,
        symbol: str,
        period: str | None = None,
        interval: str | None = None,
        use_cache: bool = True,
    ) -> pd.DataFrame:

        period = period or settings.data.default_period
        interval = interval or settings.data.default_interval

        if use_cache:

            if (
                self.cache.exists(symbol, period, interval)
                and not self.cache.is_expired(symbol, period, interval)
            ):

                cached = self.cache.load(
                    symbol,
                    period,
                    interval,
                )

                if cached is not None:
                    return cached

        df = self._download(
            symbol,
            period,
            interval,
        )

        if use_cache:
            self.cache.save(
                df,
                symbol,
                period,
                interval,
            )

        return df

    # ------------------------------------------------------------------
    # Latest Price
    # ------------------------------------------------------------------

    def get_price(
        self,
        symbol: str,
    ) -> float:

        df = self.get_history(
            symbol=symbol,
            period="5d",
            interval="1d",
        )

        return float(df["Close"].iloc[-1])

    # ------------------------------------------------------------------
    # Cache Utilities
    # ------------------------------------------------------------------

    def clear_cache(self) -> None:

        self.cache.clear()

    def refresh_cache(
        self,
        symbol: str,
        period: str | None = None,
        interval: str | None = None,
    ) -> pd.DataFrame:

        period = period or settings.data.default_period
        interval = interval or settings.data.default_interval

        self.cache.delete(
            symbol,
            period,
            interval,
        )

        return self.get_history(
            symbol,
            period,
            interval,
            use_cache=True,
        )