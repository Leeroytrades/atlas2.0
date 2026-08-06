"""
Atlas AI Trading Platform 4.0

Monte Carlo Robustness Engine

Professional validation layer.

Tests:

- Random trade ordering
- Bootstrap sampling
- Return distribution
- Drawdown risk
- Failure probability
- Strategy stability
"""

from __future__ import annotations


import random
import statistics

from dataclasses import dataclass





@dataclass
class MonteCarloResult:


    simulations: int

    trades_tested: int

    average_profit: float

    median_profit: float

    worst_profit: float

    best_profit: float

    percentile_5_profit: float

    percentile_95_profit: float

    average_drawdown: float

    worst_drawdown: float

    losing_probability: float

    drawdown_failure_probability: float

    average_trade: float

    win_rate: float

    robustness_score: float





class MonteCarloAnalyzer:


    def __init__(

        self,

        starting_cash: float = 100000.0,

        max_drawdown_limit: float = 25,

    ):

        self.starting_cash = starting_cash

        self.max_drawdown_limit = max_drawdown_limit





    def run(

        self,

        trades,

        simulations: int = 10000,

    ):


        if not trades:

            return MonteCarloResult(

                0,0,0,0,0,0,0,0,
                0,0,100,100,0,0,0

            )



        profits = [

            float(t.profit_loss)

            for t in trades

        ]



        results=[]

        drawdowns=[]



        for _ in range(simulations):


            sample=random.choices(

                profits,

                k=len(profits)

            )


            random.shuffle(sample)



            equity=self.starting_cash

            peak=equity

            max_dd=0



            for profit in sample:


                equity += profit


                peak=max(

                    peak,

                    equity

                )


                dd=(

                    (peak-equity)

                    /

                    peak

                )*100


                max_dd=max(

                    max_dd,

                    dd

                )



            results.append(

                equity-self.starting_cash

            )


            drawdowns.append(

                max_dd

            )



        results.sort()



        losing=sum(

            1

            for x in results

            if x < 0

        )



        dd_fail=sum(

            1

            for x in drawdowns

            if x > self.max_drawdown_limit

        )



        wins=sum(

            1

            for x in profits

            if x>0

        )



        win_rate=(

            wins/

            len(profits)

        )*100



        robustness=self.calculate_score(

            results,

            drawdowns

        )



        return MonteCarloResult(

            simulations,

            len(profits),

            round(statistics.mean(results),2),

            round(statistics.median(results),2),

            round(results[0],2),

            round(results[-1],2),

            round(results[int(simulations*0.05)],2),

            round(results[int(simulations*0.95)],2),

            round(statistics.mean(drawdowns),2),

            round(max(drawdowns),2),

            round(

                losing/simulations*100,

                2

            ),

            round(

                dd_fail/simulations*100,

                2

            ),

            round(

                statistics.mean(profits),

                2

            ),

            round(win_rate,2),

            round(robustness,2)

        )





    def calculate_score(

        self,

        results,

        drawdowns

    ):


        score=100



        loss_probability=(

            sum(

                1

                for x in results

                if x<0

            )

            /

            len(results)

        )*100



        score-=loss_probability



        if max(drawdowns)>30:

            score-=30


        elif max(drawdowns)>20:

            score-=15



        volatility=statistics.stdev(results)



        if volatility > abs(statistics.mean(results)):

            score-=20



        return max(

            0,

            score

        )





def print_monte_carlo_report(

    result: MonteCarloResult

):


    print()

    print("="*60)

    print("MONTE CARLO ROBUSTNESS REPORT")

    print("="*60)



    print()

    print(f"Simulations: {result.simulations}")

    print(f"Trades Tested: {result.trades_tested}")



    print()

    print("RETURN DISTRIBUTION")

    print("-"*60)

    print(f"Average Profit: ${result.average_profit:,.2f}")

    print(f"Median Profit: ${result.median_profit:,.2f}")

    print(f"Worst Case: ${result.worst_profit:,.2f}")

    print(f"Best Case: ${result.best_profit:,.2f}")

    print(f"5th Percentile: ${result.percentile_5_profit:,.2f}")

    print(f"95th Percentile: ${result.percentile_95_profit:,.2f}")



    print()

    print("RISK")

    print("-"*60)

    print(f"Average Drawdown: {result.average_drawdown:.2f}%")

    print(f"Worst Drawdown: {result.worst_drawdown:.2f}%")

    print(f"Loss Probability: {result.losing_probability:.2f}%")

    print(f"DD Failure Probability: {result.drawdown_failure_probability:.2f}%")



    print()

    print("TRADE QUALITY")

    print("-"*60)

    print(f"Average Trade: ${result.average_trade:,.2f}")

    print(f"Win Rate: {result.win_rate:.2f}%")



    print()

    print(

        f"ROBUSTNESS SCORE: {result.robustness_score:.2f}/100"

    )



    print("="*60)
