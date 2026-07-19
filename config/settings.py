"""
Atlas AI Trading Assistant 2.0

Global application configuration.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


# =============================================================================
# Risk Management
# =============================================================================

@dataclass(slots=True)
class RiskSettings:
    """Risk management configuration."""

    risk_per_trade: float = 0.01          # 1%
    max_daily_loss: float = 0.03          # 3%
    max_open_positions: int = 5
    reward_risk_ratio: float = 2.0
    max_position_size: float = 0.20       # 20% of account


# =============================================================================
# Scoring Engine
# =============================================================================

@dataclass(slots=True)
class ScoreSettings:
    """Bull/Bear scoring thresholds."""

    strong_buy: int = 80
    buy: int = 60
    neutral_low: int = -20
    neutral_high: int = 20
    sell: int = -60
    strong_sell: int = -80


# =============================================================================
# Market Data
# =============================================================================

@dataclass(slots=True)
class DataSettings:
    """Historical data defaults."""

    default_period: str = "2y"
    default_interval: str = "1d"

    cache_directory: Path = Path("data/cache")


# =============================================================================
# Backtesting
# =============================================================================

@dataclass(slots=True)
class BacktestSettings:
    initial_cash: float = 100_000.0
    commission: float = 0.001
    slippage: float = 0.0005


# =============================================================================
# Console
# =============================================================================

@dataclass(slots=True)
class ConsoleSettings:
    use_colour: bool = True
    refresh_rate: int = 1
    show_banner: bool = True


# =============================================================================
# Root Settings
# =============================================================================

@dataclass(slots=True)
class Settings:

    risk: RiskSettings = field(default_factory=RiskSettings)

    scoring: ScoreSettings = field(default_factory=ScoreSettings)

    data: DataSettings = field(default_factory=DataSettings)

    backtest: BacktestSettings = field(default_factory=BacktestSettings)

    console: ConsoleSettings = field(default_factory=ConsoleSettings)


settings = Settings()