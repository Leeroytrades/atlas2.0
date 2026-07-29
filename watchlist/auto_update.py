"""
Atlas AI Trading Assistant 3.0

Automatic Watchlist Updater

Updates the active trading universe
from Atlas market analytics.
"""

from __future__ import annotations

from pathlib import Path



WATCHLIST_FILE = Path(
    "watchlist.txt"
)



class AutoWatchlistUpdater:


    def __init__(
        self,
        symbols: list[str]
    ):

        self.symbols = symbols



    def update(self):

        """
        Replace watchlist.txt
        with Atlas selected markets.
        """


        with WATCHLIST_FILE.open(
            "w",
            encoding="utf-8"
        ) as file:


            file.write(
                "# Atlas Generated Watchlist\n"
            )


            file.write(
                "# Auto updated by Market Selector\n\n"
            )


            for symbol in self.symbols:

                file.write(
                    f"{symbol}\n"
                )


        return self.symbols