"""
Atlas AI Trading Platform

Central configuration.

Every configurable value in Atlas should live here.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class AtlasConfig:
    """Application configuration."""

    # ------------------------------------------------------------------
    # General
    # ------------------------------------------------------------------

    APP_NAME: str = "Atlas AI Trading Platform"
    VERSION: str = "2.1.0"

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------

    DATABASE_FILE: Path = Path("atlas.db")

    # ------------------------------------------------------------------
    # Trading
    # ------------------------------------------------------------------

    ACCOUNT_SIZE: float = 10_000.00
    RISK_PERCENT: float = 1.0

    # ------------------------------------------------------------------
    # Market Data
    # ------------------------------------------------------------------

    DEFAULT_PERIOD: str = "6mo"

    DEFAULT_INTERVAL: str = "1d"

    # ------------------------------------------------------------------
    # Scanner
    # ------------------------------------------------------------------

    MAX_SYMBOLS: int = 100

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    LOG_LEVEL: str = "INFO"

    LOG_FILE: str = "atlas.log"


config = AtlasConfig()