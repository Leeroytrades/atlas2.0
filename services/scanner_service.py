"""
Atlas AI Trading Platform

Scanner Service

Responsible for scanning the market watchlist.
"""

from __future__ import annotations

from atlas.scanner import Scanner
from atlas.session import Session


class ScannerService:
    """
    Handles all market scanning.
    """

    def __init__(
        self,
        session: Session,
        scanner: Scanner,
    ):

        self.session = session

        self.scanner = scanner

    def scan(self):
        """
        Scan the active watchlist.
        """

        return self.scanner.scan(
            self.session.watchlist.all()
        )