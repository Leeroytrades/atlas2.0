"""
Atlas AI Trading Platform 4.1

Trade Analytics Engine

Analyses backtest results:

- Strategy performance
- Regime performance
- Win/loss quality
- Holding periods
- Long vs short performance
- Profit concentration
- Trade expectancy

Designed for:

- Research
- Optimisation
- Walk-forward analysis
- White paper reporting
"""

from __future__ import annotations


from collections import defaultdict



class TradeAnalyser:


    def __init__(self, trades):

        self.trades = trades



    # =====================================================
    # BASIC COUNTS
    # =====================================================

    def summary(self):


        total = len(self.trades)


        wins = [

            t for t in self.trades

            if t.result == "WIN"

        ]


        losses = [

            t for t in self.trades

            if t.result == "LOSS"

        ]


        profit = sum(

            t.profit_loss

            for t in self.trades

        )


        winning_profit = sum(

            t.profit_loss

            for t in wins

        )


        losing_profit = abs(sum(

            t.profit_loss

            for t in losses

        ))



        expectancy = 0


        if total:

            expectancy = profit / total



        profit_factor = 0


        if losing_profit > 0:

            profit_factor = (

                winning_profit

                /

                losing_profit

            )



        return {


            "total_trades": total,


            "wins": len(wins),


            "losses": len(losses),


            "win_rate":

                round(

                    len(wins) / total * 100,

                    2

                )

                if total

                else 0,


            "expectancy":

                round(expectancy,2),


            "profit_factor":

                round(profit_factor,2),

        }



    # =====================================================
    # LONG / SHORT ANALYSIS
    # =====================================================

    def direction_stats(self):


        output = defaultdict(list)



        for trade in self.trades:


            output[trade.direction].append(

                trade

            )



        results = {}



        for direction, trades in output.items():


            profit = sum(

                t.profit_loss

                for t in trades

            )


            wins = sum(

                1

                for t in trades

                if t.result == "WIN"

            )



            results[direction] = {


                "trades":

                    len(trades),


                "wins":

                    wins,


                "win_rate":

                    round(

                        wins / len(trades) * 100,

                        2

                    ),


                "profit":

                    round(

                        profit,

                        2

                    ),

            }



        return results



    # =====================================================
    # HOLDING PERIOD
    # =====================================================

    def holding_stats(self):


        if not self.trades:

            return {}



        durations = [

            t.candles_held

            for t in self.trades

        ]



        winners = [

            t.candles_held

            for t in self.trades

            if t.result == "WIN"

        ]



        losers = [

            t.candles_held

            for t in self.trades

            if t.result == "LOSS"

        ]



        return {


            "average_hold":

                round(

                    sum(durations)

                    /

                    len(durations),

                    2

                ),


            "average_winner_hold":

                round(

                    sum(winners)

                    /

                    len(winners),

                    2

                )

                if winners

                else 0,


            "average_loser_hold":

                round(

                    sum(losers)

                    /

                    len(losers),

                    2

                )

                if losers

                else 0,

        }



    # =====================================================
    # BIG WIN DEPENDENCY
    # =====================================================

    def profit_concentration(self):


        if not self.trades:

            return {}



        sorted_trades = sorted(

            self.trades,

            key=lambda x: x.profit_loss,

            reverse=True

        )



        top_5 = sorted_trades[:5]



        total_profit = sum(

            t.profit_loss

            for t in self.trades

        )


        top_profit = sum(

            t.profit_loss

            for t in top_5

        )



        concentration = 0



        if total_profit > 0:

            concentration = (

                top_profit

                /

                total_profit

                *

                100

            )



        return {


            "top_5_profit":

                round(top_profit,2),


            "profit_dependency_percent":

                round(

                    concentration,

                    2

                ),

        }



    # =====================================================
    # FULL REPORT
    # =====================================================

    def report(self):


        return {


            "summary":

                self.summary(),


            "direction":

                self.direction_stats(),


            "holding":

                self.holding_stats(),


            "profit_concentration":

                self.profit_concentration(),

        }