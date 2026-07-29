"""
Atlas AI Trading Assistant 2.0

Watchlist Manager
"""

from __future__ import annotations

from pathlib import Path


# watchlist.txt is located in the project root (same folder as main.py)
WATCHLIST_FILE = Path(__file__).parent.parent / "watchlist.txt"



class Watchlist:
    """
    Loads and manages the trading watchlist.
    """



    def __init__(self):

        self.symbols = self._load()



    def _load(self) -> list[str]:
        """
        Load symbols from watchlist.txt.
        """

        # Create default watchlist if missing

        if not WATCHLIST_FILE.exists():

            default_symbols = [

                "AAPL",
                "MSFT",
                "NVDA",
                "META",
                "GOOGL",
                "AMZN",
                "TSLA",
                "AMD",
                "NFLX",
                "PLTR",
                "SPY",
                "QQQ",

            ]


            with WATCHLIST_FILE.open(
                "w",
                encoding="utf-8"
            ) as f:

                for symbol in default_symbols:

                    f.write(symbol + "\n")



        symbols = []


        with WATCHLIST_FILE.open(
            "r",
            encoding="utf-8"
        ) as f:


            for line in f:


                symbol = line.strip().upper()



                # Ignore blanks and comments

                if symbol and not symbol.startswith("#"):

                    symbols.append(symbol)



        # Remove duplicates preserving order

        return list(
            dict.fromkeys(symbols)
        )



    def _save(self):

        """
        Save watchlist to disk.
        """

        with WATCHLIST_FILE.open(
            "w",
            encoding="utf-8"
        ) as f:


            for symbol in self.symbols:

                f.write(
                    symbol + "\n"
                )



    def reload(self):

        """
        Reload watchlist from file.
        """

        self.symbols = self._load()



    def all(self) -> list[str]:

        """
        Return all symbols.
        """

        return self.symbols



    def add(
        self,
        symbol: str
    ):

        """
        Add a symbol.
        """

        symbol = symbol.strip().upper()



        if symbol and symbol not in self.symbols:

            self.symbols.append(
                symbol
            )

            self._save()



    def remove(
        self,
        symbol: str
    ):

        """
        Remove a symbol.
        """

        symbol = symbol.strip().upper()



        if symbol in self.symbols:

            self.symbols.remove(
                symbol
            )

            self._save()



    def update(
        self,
        symbols: list[str]
    ):

        """
        Replace the entire watchlist.

        Used by Atlas market selection
        to automatically update active markets.
        """

        cleaned = []



        for symbol in symbols:


            symbol = symbol.strip().upper()



            if symbol and symbol not in cleaned:

                cleaned.append(
                    symbol
                )



        self.symbols = cleaned



        self._save()