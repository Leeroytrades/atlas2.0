"""
Atlas AI Trading Platform 4.1

Trade Analysis Engine

Research layer for backtesting.

Provides:

- Performance statistics
- Long / short analysis
- Strategy contribution
- Win/loss distribution
- Profit concentration
- Streak analysis
- Holding time analysis
"""

from __future__ import annotations


from collections import defaultdict



class TradeAnalyzer:


    def __init__(self, trades):

        self.trades = trades



    # =====================================================
    # FILTERS
    # =====================================================

    def wins(self):

        return [

            t for t in self.trades

            if t.profit_loss > 0

        ]



    def losses(self):

        return [

            t for t in self.trades

            if t.profit_loss < 0

        ]



    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(self):


        total = len(self.trades)

        wins = len(self.wins())

        losses = len(self.losses())


        profit = sum(

            t.profit_loss

            for t in self.trades

        )


        gross_profit = sum(

            t.profit_loss

            for t in self.wins()

        )


        gross_loss = abs(sum(

            t.profit_loss

            for t in self.losses()

        ))


        return {


            "trades": total,

            "wins": wins,

            "losses": losses,


            "win_rate":

                round(

                    wins / total * 100,

                    2

                )

                if total else 0,


            "profit":

                round(

                    profit,

                    2

                ),


            "profit_factor":

                round(

                    gross_profit / gross_loss,

                    2

                )

                if gross_loss else 0,


            "expectancy":

                round(

                    profit / total,

                    2

                )

                if total else 0,

        }



    # =====================================================
    # DIRECTION ANALYSIS
    # =====================================================

    def direction_analysis(self):


        result = defaultdict(

            lambda: {

                "trades": 0,

                "wins": 0,

                "profit": 0,

            }

        )


        for trade in self.trades:


            data = result[trade.direction]


            data["trades"] += 1


            if trade.profit_loss > 0:

                data["wins"] += 1


            data["profit"] += trade.profit_loss



        for data in result.values():


            data["profit"] = round(

                data["profit"],

                2

            )


            data["win_rate"] = (

                round(

                    data["wins"]

                    /

                    data["trades"]

                    *

                    100,

                    2

                )

                if data["trades"]

                else 0

            )



        return dict(result)



    # =====================================================
    # STRATEGY ANALYSIS
    # =====================================================

    def strategy_analysis(self):


        result = defaultdict(

            lambda: {

                "trades": 0,

                "wins": 0,

                "profit": 0,

            }

        )


        for trade in self.trades:


            strategy = getattr(

                trade,

                "strategy",

                "UNKNOWN"

            )


            data = result[strategy]


            data["trades"] += 1


            if trade.profit_loss > 0:

                data["wins"] += 1


            data["profit"] += trade.profit_loss



        for data in result.values():


            data["profit"] = round(

                data["profit"],

                2

            )


            data["win_rate"] = (

                round(

                    data["wins"]

                    /

                    data["trades"]

                    *

                    100,

                    2

                )

                if data["trades"]

                else 0

            )



        return dict(result)



    # =====================================================
    # DISTRIBUTION
    # =====================================================

    def distribution(self):


        winners = [

            t.profit_loss

            for t in self.wins()

        ]


        losers = [

            t.profit_loss

            for t in self.losses()

        ]



        return {


            "average_winner":

                round(

                    sum(winners)

                    /

                    len(winners),

                    2

                )

                if winners else 0,


            "average_loser":

                round(

                    sum(losers)

                    /

                    len(losers),

                    2

                )

                if losers else 0,


            "largest_winner":

                round(

                    max(winners),

                    2

                )

                if winners else 0,


            "largest_loser":

                round(

                    min(losers),

                    2

                )

                if losers else 0,

        }



    # =====================================================
    # PROFIT CONCENTRATION
    # =====================================================

    def profit_concentration(self, count=5):


        profits = sorted(

            [

                t.profit_loss

                for t in self.trades

            ],

            reverse=True

        )


        total = sum(profits)


        top_profit = sum(

            profits[:count]

        )


        return {


            "top_trades":

                round(

                    top_profit,

                    2

                ),


            "dependency_percent":

                round(

                    top_profit

                    /

                    total

                    *

                    100,

                    2

                )

                if total else 0,

        }



    # =====================================================
    # STREAKS
    # =====================================================

    def streaks(self):


        max_wins = 0

        max_losses = 0


        current_wins = 0

        current_losses = 0



        for trade in self.trades:


            if trade.profit_loss > 0:


                current_wins += 1

                current_losses = 0


            else:


                current_losses += 1

                current_wins = 0



            max_wins = max(

                max_wins,

                current_wins

            )


            max_losses = max(

                max_losses,

                current_losses

            )



        return {


            "max_winning_streak":

                max_wins,


            "max_losing_streak":

                max_losses,

        }



    # =====================================================
    # HOLDING TIME
    # =====================================================

    def holding_analysis(self):


        if not self.trades:

            return {}



        winners = self.wins()

        losers = self.losses()



        return {


            "average_hold":

                round(

                    sum(

                        t.candles_held

                        for t in self.trades

                    )

                    /

                    len(self.trades),

                    2

                ),


            "winner_average_hold":

                round(

                    sum(

                        t.candles_held

                        for t in winners

                    )

                    /

                    len(winners),

                    2

                )

                if winners else 0,


            "loser_average_hold":

                round(

                    sum(

                        t.candles_held

                        for t in losers

                    )

                    /

                    len(losers),

                    2

                )

                if losers else 0,

        }



    # =====================================================
    # FULL REPORT
    # =====================================================

    def report(self):


        return {


            "summary":

                self.summary(),


            "direction":

                self.direction_analysis(),


            "strategy":

                self.strategy_analysis(),


            "distribution":

                self.distribution(),


            "profit_concentration":

                self.profit_concentration(),


            "streaks":

                self.streaks(),


            "holding":

                self.holding_analysis(),

        }