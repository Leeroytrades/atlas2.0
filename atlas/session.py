"""
Trading Session
"""

from __future__ import annotations

from atlas.watchlist import Watchlist
from atlas.portfolio import Portfolio


class Session:

    def __init__(self):

        self.watchlist = Watchlist()

        self.portfolio = Portfolio()