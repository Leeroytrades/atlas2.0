"""
Atlas AI Trading Platform 4.0

Performance Report Engine

Calculates:

- Returns
- Win rate
- Profit factor
- Expectancy
- Drawdown
- Risk metrics
- Trade distribution
- Holding statistics
- Streak analysis
- Strategy attribution

Used by:

- Backtesting
- Walk Forward Validation
- Research Reports
- Optimisation
"""

from __future__ import annotations


from typing import List, Dict, Any

import math



class PerformanceReport:


    def __init__(

        self,

        trades,

        starting_cash: float = 100000.0,

        equity_curve=None,

    ):


        self.trades = trades or []

        self.starting_cash = starting_cash

        self.equity_curve = equity_curve or []



    # =====================================================
    # BASIC STATS
    # =====================================================

    def summary(self):


        total = len(self.trades)


        wins = [

            t for t in self.trades

            if t.profit_loss > 0

        ]


        losses = [

            t for t in self.trades

            if t.profit_loss < 0

        ]



        profit = sum(

            t.profit_loss

            for t in self.trades

        )


        gross_profit = sum(

            t.profit_loss

            for t in wins

        )


        gross_loss = abs(

            sum(

                t.profit_loss

                for t in losses

            )

        )



        win_rate = (

            len(wins)

            /

            total

            *

            100

            if total

            else 0

        )



        profit_factor = (

            gross_profit / gross_loss

            if gross_loss

            else 0

        )



        expectancy = (

            profit / total

            if total

            else 0

        )



        return {


            "trades":

                total,


            "wins":

                len(wins),


            "losses":

                len(losses),


            "win_rate":

                round(win_rate,2),


            "profit":

                round(profit,2),


            "profit_factor":

                round(profit_factor,2),


            "expectancy":

                round(expectancy,2),

        }



    # =====================================================
    # RETURNS
    # =====================================================

    def returns(self):


        ending = (

            self.equity_curve[-1]

            if self.equity_curve

            else self.starting_cash

        )


        profit = ending - self.starting_cash


        percentage = (

            profit

            /

            self.starting_cash

            *

            100

        )



        return {


            "starting":

                round(

                    self.starting_cash,

                    2

                ),


            "ending":

                round(

                    ending,

                    2

                ),


            "profit":

                round(

                    profit,

                    2

                ),


            "return_percent":

                round(

                    percentage,

                    2

                ),

        }



    # =====================================================
    # DRAWDOWN
    # =====================================================

    def drawdown(self):


        if not self.equity_curve:

            return 0



        peak = self.equity_curve[0]


        maximum = 0



        for value in self.equity_curve:


            if value > peak:

                peak=value



            decline = (

                peak-value

            ) / peak * 100



            maximum=max(

                maximum,

                decline

            )



        return round(

            maximum,

            2

        )



    # =====================================================
    # TRADE DISTRIBUTION
    # =====================================================

    def distribution(self):


        winners = [

            t.profit_loss

            for t in self.trades

            if t.profit_loss > 0

        ]


        losers = [

            t.profit_loss

            for t in self.trades

            if t.profit_loss < 0

        ]



        return {


            "average_winner":

                round(

                    sum(winners)/len(winners)

                    if winners else 0,

                    2

                ),


            "average_loser":

                round(

                    sum(losers)/len(losers)

                    if losers else 0,

                    2

                ),


            "largest_winner":

                round(

                    max(winners)

                    if winners else 0,

                    2

                ),


            "largest_loser":

                round(

                    min(losers)

                    if losers else 0,

                    2

                ),

        }



    # =====================================================
    # HOLDING TIME
    # =====================================================

    def holding(self):


        holds = [

            t.candles_held

            for t in self.trades

        ]


        winners = [

            t.candles_held

            for t in self.trades

            if t.profit_loss > 0

        ]


        losers = [

            t.candles_held

            for t in self.trades

            if t.profit_loss < 0

        ]



        return {


            "average_hold":

                round(

                    sum(holds)/len(holds)

                    if holds else 0,

                    2

                ),


            "winner_average_hold":

                round(

                    sum(winners)/len(winners)

                    if winners else 0,

                    2

                ),


            "loser_average_hold":

                round(

                    sum(losers)/len(losers)

                    if losers else 0,

                    2

                ),

        }



    # =====================================================
    # STREAKS
    # =====================================================

    def streaks(self):


        max_win = 0

        max_loss = 0


        current_win = 0

        current_loss = 0



        for trade in self.trades:


            if trade.profit_loss > 0:


                current_win += 1

                current_loss = 0


            elif trade.profit_loss < 0:


                current_loss += 1

                current_win = 0


            max_win=max(

                max_win,

                current_win

            )


            max_loss=max(

                max_loss,

                current_loss

            )



        return {


            "max_winning_streak":

                max_win,


            "max_losing_streak":

                max_loss,

        }



    # =====================================================
    # STRATEGY BREAKDOWN
    # =====================================================

    def strategies(self):


        result={}



        for trade in self.trades:


            name=getattr(

                trade,

                "strategy",

                "UNKNOWN"

            )


            if name not in result:

                result[name]={

                    "trades":0,

                    "wins":0,

                    "profit":0,

                }



            result[name]["trades"] += 1


            result[name]["profit"] += trade.profit_loss



            if trade.profit_loss > 0:

                result[name]["wins"] += 1



        for name,data in result.items():


            data["profit"]=round(

                data["profit"],

                2

            )


            data["win_rate"]=round(

                data["wins"]

                /

                data["trades"]

                *

                100,

                2

            )



        return result



    # =====================================================
    # FULL REPORT
    # =====================================================

    def report(self):


        return {


            "summary":

                self.summary(),


            "returns":

                self.returns(),


            "drawdown":

                self.drawdown(),


            "distribution":

                self.distribution(),


            "holding":

                self.holding(),


            "streaks":

                self.streaks(),


            "strategy":

                self.strategies(),

        }