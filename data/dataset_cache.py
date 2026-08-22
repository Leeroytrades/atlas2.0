"""
Atlas AI Trading Platform 4.1

Dataset Cache

Purpose:
Load historical market data and build indicators ONCE.

The optimisation engine can then reuse the same processed
DataFrame across hundreds of strategy evaluations without
re-downloading or recalculating indicators.
"""

from __future__ import annotations

from threading import Lock

import pandas as pd

from data.market_data import MarketData
from indicators.composite import build_indicator_set


class DatasetCache:
    """In-memory cache of processed market datasets."""

    _cache: dict[str, pd.DataFrame] = {}
    _lock = Lock()

    @classmethod
    def _key(
        cls,
        symbol: str,
        period: str,
        interval: str,
    ) -> str:

        return f"{symbol}:{period}:{interval}"

    @classmethod
    def get(
        cls,
        symbol: str,
        period: str = "10y",
        interval: str = "1d",
    ) -> pd.DataFrame:
        """
        Return a processed DataFrame.

        If already cached:
            returns a COPY

        Otherwise:
            downloads once
            builds indicators once
            stores in memory
        """

        key = cls._key(symbol, period, interval)

        with cls._lock:

            if key in cls._cache:
                return cls._cache[key].copy()

        market = MarketData()

        raw = market.get_history(
            symbol=symbol,
            period=period,
            interval=interval,
        )

        processed = build_indicator_set(raw.copy())

        with cls._lock:
            cls._cache[key] = processed

        print(f"Cached dataset: {symbol} ({len(processed)} candles)")

        return processed.copy()

    @classmethod
    def preload(
        cls,
        symbols: list[str],
        period: str = "10y",
        interval: str = "1d",
    ) -> None:

        for symbol in symbols:
            cls.get(symbol, period, interval)

    @classmethod
    def clear(cls) -> None:

        with cls._lock:
            cls._cache.clear()

    @classmethod
    def stats(cls) -> dict:

        return {
            "datasets": len(cls._cache),
            "symbols": list(cls._cache.keys()),
        }