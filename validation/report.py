"""
Atlas AI Trading Platform 3.3

Validation Report Generator

Enhanced walk-forward analysis.

Includes:

- Window reporting
- Regime analysis
- Weighted validation scoring
- Robustness scoring
"""

from __future__ import annotations



class ValidationReport:



    def __init__(

        self,

        results: list[dict],

    ):

        self.results = results



    # =====================================================
    # Display Report
    # =====================================================

    def display(self):


        print()

        print("=" * 50)

        print(
            "ATLAS WALK FORWARD VALIDATION REPORT"
        )

        print("=" * 50)



        passed = 0



        valid_windows = 0



        regime_stats = {}



        for index, result in enumerate(

            self.results,

            start=1,

        ):



            window_id = result.get(

                "window_id",

                index

            )



            print()

            print(
                f"WINDOW {window_id}"
            )

            print(
                "-" * 30
            )



            training = result.get(

                "training",

                {}

            )


            validation = result.get(

                "validation",

                {}

            )



            trades = validation.get(

                "total_trades",

                0

            )



            print()

            print(
                "TRAINING"
            )


            print(

                f"Profit: ${training.get('profit',0):,.2f}"

            )


            print(

                f"Win Rate: {training.get('win_rate',0)}%"

            )


            print(

                f"Profit Factor: {training.get('profit_factor',0)}"

            )


            print(

                f"Trades: {training.get('total_trades',0)}"

            )



            print()

            print(
                "VALIDATION"
            )


            print(

                f"Profit: ${validation.get('profit',0):,.2f}"

            )


            print(

                f"Win Rate: {validation.get('win_rate',0)}%"

            )


            print(

                f"Profit Factor: {validation.get('profit_factor',0)}"

            )


            print(

                f"Trades: {trades}"

            )



            verdict = result.get(

                "verdict",

                "FAIL"

            )



            print()

            print(

                f"VERDICT: {verdict}"

            )



            if verdict == "PASS":

                passed += 1



            # -------------------------------
            # Regime Tracking
            # -------------------------------


            regime = result.get(

                "regime",

                {}

            )


            environment = regime.get(

                "regime",

                "UNKNOWN"

            )



            if environment not in regime_stats:

                regime_stats[environment] = {

                    "windows":0,

                    "profit":0,

                    "passes":0,

                }



            regime_stats[environment]["windows"] += 1


            regime_stats[environment]["profit"] += (

                validation.get(

                    "profit",

                    0

                )

            )


            if verdict == "PASS":

                regime_stats[environment]["passes"] += 1



            # Only score windows with trades

            if trades > 0:

                valid_windows += 1





        print()

        print("=" * 50)

        print(

            f"Windows: {len(self.results)}"

        )



        rate = (

            passed

            /

            len(self.results)

            *

            100

            if self.results

            else 0

        )



        print(

            f"Pass Rate: {rate:.1f}%"

        )



        print("=" * 50)



        self.display_robustness(

            valid_windows,

            regime_stats,

        )




    # =====================================================
    # Robustness Analysis
    # =====================================================

    def display_robustness(

        self,

        valid_windows,

        regime_stats,

    ):


        print()

        print("=" * 50)

        print(

            "ATLAS ROBUSTNESS ANALYSIS"

        )

        print("=" * 50)



        training_quality = self.training_quality()



        validation_quality = self.validation_quality()



        stability = self.stability_score()



        print()

        print(

            f"Training Quality: {training_quality:.1f}/100"

        )


        print(

            f"Validation Quality: {validation_quality:.1f}/100"

        )


        print(

            f"Stability Score: {stability:.1f}/100"

        )



        print()


        print(

            "REGIME PERFORMANCE"

        )


        print(

            "-" * 30

        )



        for regime, data in regime_stats.items():


            if data["windows"]:


                print()

                print(

                    regime

                )


                print(

                    f"Windows: {data['windows']}"

                )


                print(

                    f"Profit: ${data['profit']:,.2f}"

                )


                print(

                    f"Passes: {data['passes']}"

                )



        robustness = (

            training_quality

            *

            0.35

            +

            validation_quality

            *

            0.40

            +

            stability

            *

            0.25

        )



        print()

        print(

            f"ROBUSTNESS SCORE: {robustness:.2f}/100"

        )



        if robustness >= 70:

            verdict = "ACCEPT"


        elif robustness >= 50:

            verdict = "NEEDS IMPROVEMENT"


        else:

            verdict = "REJECT"



        print()

        print(

            f"VERDICT: {verdict}"

        )


        print("=" * 50)




    # =====================================================
    # Scoring
    # =====================================================

    def training_quality(self):


        score = 0


        for result in self.results:


            training = result.get(

                "training",

                {}

            )


            if training.get(

                "profit",

                0

            ) > 0:

                score += 1



        return (

            score

            /

            len(self.results)

            *

            100

            if self.results

            else 0

        )



    def validation_quality(self):


        score = 0


        count = 0


        for result in self.results:


            validation = result.get(

                "validation",

                {}

            )


            trades = validation.get(

                "total_trades",

                0

            )


            if trades < 10:

                continue



            count += 1



            if validation.get(

                "profit",

                0

            ) > 0:

                score += 1



        return (

            score

            /

            count

            *

            100

            if count

            else 0

        )



    def stability_score(self):


        scores = []


        for result in self.results:


            validation = result.get(

                "validation",

                {}

            )


            trades = validation.get(

                "total_trades",

                0

            )


            if trades < 10:

                continue



            pf = min(

                validation.get(

                    "profit_factor",

                    0

                ),

                5

            )


            scores.append(

                pf

            )



        if not scores:

            return 0



        average = sum(scores) / len(scores)



        return min(

            average

            *

            20,

            100

        )