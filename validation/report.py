"""
Atlas AI Trading Platform 3.5

Walk Forward Validation Report

Generates research reports from
validation windows.

Features:

- Aggregate performance
- Pass rate
- Robustness score
- Regime analysis
- Strategy health rating
"""

from __future__ import annotations



class ValidationReport:



    def __init__(
        self,
        results: list[dict],
    ):

        self.results = results



    # =====================================================
    # Aggregate Metrics
    # =====================================================

    def aggregate(self):


        total_profit = 0

        total_trades = 0

        wins = 0

        losses = 0


        gross_profit = 0

        gross_loss = 0



        for result in self.results:


            validation = result.get(
                "validation",
                {}
            )


            profit = validation.get(
                "profit",
                0
            )


            trades = validation.get(
                "total_trades",
                0
            )


            total_profit += profit

            total_trades += trades


            wins += validation.get(
                "winning_trades",
                0
            )


            losses += validation.get(
                "losing_trades",
                0
            )


            if profit > 0:

                gross_profit += profit

            else:

                gross_loss += abs(
                    profit
                )



        profit_factor = (

            gross_profit / gross_loss

            if gross_loss > 0

            else 0

        )


        win_rate = (

            wins /
            (wins + losses)
            *
            100

            if wins + losses > 0

            else 0

        )


        return {


            "profit":

                round(
                    total_profit,
                    2
                ),


            "trades":

                total_trades,


            "wins":

                wins,


            "losses":

                losses,


            "win_rate":

                round(
                    win_rate,
                    2
                ),


            "profit_factor":

                round(
                    profit_factor,
                    2
                ),


        }



    # =====================================================
    # Robustness Score
    # =====================================================

    def robustness_score(self):


        score = 0



        passed = sum(

            1

            for r in self.results

            if r.get(
                "verdict"
            )
            ==
            "PASS"

        )



        total = len(
            self.results
        )



        if total:


            score += (

                passed /

                total

                *

                40

            )



        aggregate = self.aggregate()



        if aggregate["profit"] > 0:

            score += 20



        if aggregate["profit_factor"] >= 2:

            score += 25


        elif aggregate["profit_factor"] >= 1.5:

            score += 15


        elif aggregate["profit_factor"] >= 1:

            score += 5



        if aggregate["trades"] >= 50:

            score += 15


        elif aggregate["trades"] >= 20:

            score += 10



        return round(

            min(
                score,
                100
            ),

            2

        )



    # =====================================================
    # Regime Analysis
    # =====================================================

    def regime_analysis(self):


        regimes = {}



        for result in self.results:


            regime = result.get(
                "regime",
                "UNKNOWN"
            )


            if isinstance(
                regime,
                dict
            ):

                regime_name = str(
                    regime
                )

            else:

                regime_name = regime



            if regime_name not in regimes:

                regimes[regime_name] = {


                    "windows": 0,

                    "passes": 0,


                }



            regimes[regime_name]["windows"] += 1



            if result.get(
                "verdict"
            ) == "PASS":

                regimes[regime_name]["passes"] += 1



        return regimes



    # =====================================================
    # Print Report
    # =====================================================

    def display(self):


        aggregate = self.aggregate()



        passed = sum(

            1

            for r in self.results

            if r.get(
                "verdict"
            )
            ==
            "PASS"

        )


        total = len(
            self.results
        )



        print()

        print("=" * 60)

        print(
            "ATLAS WALK FORWARD REPORT"
        )

        print("=" * 60)



        print()

        print(
            f"Total Windows: {total}"
        )


        print(
            f"Passed: {passed}"
        )


        print(
            f"Failed: {total-passed}"
        )


        print(

            f"Pass Rate: "

            f"{(passed/total*100):.1f}%"

            if total

            else

            "Pass Rate: 0%"

        )



        print()

        print("-" * 60)

        print(
            "COMBINED VALIDATION PERFORMANCE"
        )

        print("-" * 60)



        print(
            f"Profit: {aggregate['profit']}"
        )


        print(
            f"Trades: {aggregate['trades']}"
        )


        print(
            f"Win Rate: {aggregate['win_rate']}%"
        )


        print(
            f"Profit Factor: {aggregate['profit_factor']}"
        )



        print()

        print("-" * 60)

        print(
            "ROBUSTNESS SCORE"
        )

        print("-" * 60)



        print(

            f"{self.robustness_score()}/100"

        )



        print()

        print("-" * 60)

        print(
            "REGIME ANALYSIS"
        )

        print("-" * 60)



        for regime, data in self.regime_analysis().items():


            print()

            print(
                regime
            )


            print(
                f"Windows: {data['windows']}"
            )


            print(
                f"Passes: {data['passes']}"
            )



        print()