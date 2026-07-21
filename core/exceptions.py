"""
Atlas custom exceptions.
"""


class AtlasError(Exception):
    """Base Atlas exception."""


class DatabaseError(AtlasError):
    """Database error."""


class MarketDataError(AtlasError):
    """Market data error."""


class StrategyError(AtlasError):
    """Strategy error."""


class RiskError(AtlasError):
    """Risk calculation error."""


class ExecutionError(AtlasError):
    """Execution engine error."""