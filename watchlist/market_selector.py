"""
Atlas AI Trading Assistant 3.0

Market Selector

Creates an active trading watchlist
from backtest analytics rankings.
"""

from __future__ import annotations



class MarketSelector:


    def __init__(
        self,
        rankings: list[dict],
        minimum_score: float = 60,
        maximum_markets: int = 5
    ):

        self.rankings = rankings

        self.minimum_score = minimum_score

        self.maximum_markets = maximum_markets



    def select(self) -> list[str]:

        """
        Return strongest markets only.
        """


        selected = []


        for market in self.rankings:


            if market["score"] < self.minimum_score:

                continue



            if market["profit_factor"] == "INF":

                continue



            selected.append(

                market["symbol"]

            )



            if len(selected) >= self.maximum_markets:

                break



        return selected



    def report(self):

        """
        Human readable selection report.
        """


        selected = self.select()



        return {

            "selected_markets": selected,

            "count": len(selected),

            "criteria": {

                "minimum_score": self.minimum_score,

                "maximum_markets": self.maximum_markets

            }

        }