"""
Atlas AI Trading Assistant

Cache Manager

Responsible for:

- Loading cached market data
- Saving cached market data
- Cache validation
- Cache expiry
"""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import tempfile

import pandas as pd

from config.settings import settings


class CacheManager:
    """Market data cache."""

    def __init__(self) -> None:

        self.cache_dir = Path(settings.data.cache_directory)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def cache_path(
        self,
        symbol: str,
        period: str,
        interval: str,
    ) -> Path:

        filename = f"{symbol.upper()}_{period}_{interval}.parquet"

        return self.cache_dir / filename

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def exists(
        self,
        symbol: str,
        period: str,
        interval: str,
    ) -> bool:

        return self.cache_path(
            symbol,
            period,
            interval,
        ).exists()

    def is_expired(
        self,
        symbol: str,
        period: str,
        interval: str,
    ) -> bool:

        path = self.cache_path(
            symbol,
            period,
            interval,
        )

        if not path.exists():
            return True

        modified = datetime.fromtimestamp(path.stat().st_mtime)

        age = datetime.now() - modified

        return age > timedelta(
            hours=settings.data.cache_expiry_hours,
        )

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def load(
        self,
        symbol: str,
        period: str,
        interval: str,
    ) -> pd.DataFrame | None:

        path = self.cache_path(
            symbol,
            period,
            interval,
        )

        if not path.exists():
            return None

        try:

            return pd.read_parquet(path)

        except Exception:

            try:
                path.unlink()
            except OSError:
                pass

            return None

    # ------------------------------------------------------------------
    # Saving
    # ------------------------------------------------------------------

    def save(
        self,
        df: pd.DataFrame,
        symbol: str,
        period: str,
        interval: str,
    ) -> None:

        destination = self.cache_path(
            symbol,
            period,
            interval,
        )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".parquet",
            dir=self.cache_dir,
        ) as temp:

            temp_path = Path(temp.name)

        try:

            df.to_parquet(temp_path)

            temp_path.replace(destination)

        finally:

            if temp_path.exists():
                temp_path.unlink(missing_ok=True)

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    def delete(
        self,
        symbol: str,
        period: str,
        interval: str,
    ) -> None:

        path = self.cache_path(
            symbol,
            period,
            interval,
        )

        if path.exists():
            path.unlink()

    def clear(self) -> None:

        for file in self.cache_dir.glob("*.parquet"):
            file.unlink()