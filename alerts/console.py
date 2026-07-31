"""
Atlas AI Trading Platform

Console Alerts
"""

from __future__ import annotations



class ConsoleAlert:


    def send(
        self,
        message: str,
    ):

        print()

        print(
            f"[ATLAS ALERT] {message}"
        )

        print()