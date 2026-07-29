"""
Atlas AI Trading Assistant 3.0

Backtest Analytics

Ranks markets based on performance.
"""

from __future__ import annotations



class MarketAnalytics:


    def __init__(
        self,
        results: dict
    ):

        self.results = results



    def rank_markets(self):

        rankings = []


        for symbol, data in self.results.items():


            profit = data["net_profit"]

            win_rate = data["win_rate"]

            profit_factor = data["profit_factor"]

            trades = data["total_trades"]



            # Ignore markets with no trades

            if trades == 0:

                continue



            score = 0



            # Profit

            if profit > 0:

                score += 40


            else:

                score -= 20



            # Win rate

            score += min(

                win_rate,

                60

            ) / 2



            # Profit factor

            if isinstance(
                profit_factor,
                float
            ):

                score += min(

                    profit_factor * 10,

                    30

                )



            # Trade reliability

            if trades >= 20:

                score += 10



            elif trades < 5:

                score -= 10



            rankings.append(

                {

                    "symbol": symbol,

                    "score": round(

                        score,

                        2

                    ),

                    "profit": profit,

                    "trades": trades,

                    "win_rate": win_rate,

                    "profit_factor": profit_factor

                }

            )



        return sorted(

            rankings,

            key=lambda x: x["score"],

            reverse=True

        )



    def best_markets(
        self,
        count=3
    ):

        return self.rank_markets()[:count]