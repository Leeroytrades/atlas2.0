"""
Atlas AI Trading Platform 3.3

Validation Robustness Scoring Engine

Evaluates whether a strategy
is likely robust or overfit.

Does not modify:
- Optimiser
- Backtester
- Simulator

Only analyses validation results.
"""

from __future__ import annotations



class RobustnessAnalyzer:



    def __init__(

        self,

        results: list[dict],

    ):

        self.results = results



    # =====================================================
    # Score individual performance
    # =====================================================

    def performance_score(

        self,

        metrics: dict,

    ):


        score = 0



        profit = metrics.get(

            "profit",

            metrics.get(

                "net_profit",

                0

            )

        )



        profit_factor = metrics.get(

            "profit_factor",

            0

        )



        trades = metrics.get(

            "total_trades",

            metrics.get(

                "trades",

                0

            )

        )



        win_rate = metrics.get(

            "win_rate",

            0

        )



        # Profit

        if profit > 0:

            score += 30



        # Profit factor

        if profit_factor >= 2:

            score += 30

        elif profit_factor >= 1.5:

            score += 20

        elif profit_factor >= 1:

            score += 10



        # Trade reliability

        if trades >= 100:

            score += 20

        elif trades >= 50:

            score += 15

        elif trades >= 20:

            score += 10



        # Win rate

        if win_rate >= 50:

            score += 20

        elif win_rate >= 35:

            score += 10



        return min(

            score,

            100

        )



    # =====================================================
    # Stability
    # =====================================================

    def stability_score(self):


        scores = []



        for result in self.results:


            validation = result.get(

                "validation",

                {}

            )


            scores.append(

                self.performance_score(

                    validation

                )

            )



        if not scores:

            return 0



        average = sum(scores) / len(scores)



        failures = scores.count(0)



        penalty = failures * 15



        return max(

            0,

            round(

                average - penalty,

                2

            )

        )



    # =====================================================
    # Complete Analysis
    # =====================================================

    def analyse(self):


        training_scores = []

        validation_scores = []



        for result in self.results:



            training_scores.append(

                self.performance_score(

                    result.get(

                        "training",

                        {}

                    )

                )

            )



            validation_scores.append(

                self.performance_score(

                    result.get(

                        "validation",

                        {}

                    )

                )

            )



        training_quality = (

            sum(training_scores)

            /

            len(training_scores)

            if training_scores

            else 0

        )



        validation_quality = (

            sum(validation_scores)

            /

            len(validation_scores)

            if validation_scores

            else 0

        )



        stability = self.stability_score()



        final_score = round(

            (

                validation_quality * 0.5

                +

                stability * 0.3

                +

                training_quality * 0.2

            ),

            2

        )



        if final_score >= 75:

            verdict = "PASS"



        elif final_score >= 50:

            verdict = "REVIEW"



        else:

            verdict = "REJECT"



        return {


            "training_quality":

                round(

                    training_quality,

                    2

                ),


            "validation_quality":

                round(

                    validation_quality,

                    2

                ),


            "stability":

                stability,


            "robustness_score":

                final_score,


            "verdict":

                verdict,

        }



    # =====================================================
    # Display
    # =====================================================

    def display(self):


        report = self.analyse()



        print()

        print("=" * 50)

        print(

            "ATLAS ROBUSTNESS ANALYSIS"

        )

        print("=" * 50)



        print()

        print(

            f"Training Quality: "

            f"{report['training_quality']}/100"

        )



        print(

            f"Validation Quality: "

            f"{report['validation_quality']}/100"

        )



        print(

            f"Stability Score: "

            f"{report['stability']}/100"

        )



        print()

        print(

            f"ROBUSTNESS SCORE: "

            f"{report['robustness_score']}/100"

        )



        print()

        print(

            f"VERDICT: "

            f"{report['verdict']}"

        )



        print("=" * 50)