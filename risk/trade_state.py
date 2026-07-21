"""
Atlas AI Trading Assistant 2.1

Trade State Management
"""

from enum import Enum


class TradeState(str, Enum):

    OPEN = "OPEN"

    TARGET_HIT = "TARGET_HIT"

    STOPPED = "STOPPED"

    CLOSED = "CLOSED"