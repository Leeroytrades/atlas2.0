"""
Atlas AI Trading Platform 3.7

Benchmark Comparison Engine

Compares Atlas performance against
simple buy-and-hold investing.

Includes:

- Benchmark return
- Final equity
- Alpha generation
- Drawdown comparison
- Risk improvement
- Verdict
"""


from __future__ import annotations


from dataclasses import dataclass

import pandas as pd



@dataclass
class BenchmarkReport:

    symbol: str

    starting_cash: float

    benchmark_final_equity: float

    benchmark_return: float

    benchmark_drawdown: float

    atlas_final_equity: float

    atlas_return: float

    atlas_drawdown: float

    alpha: float

    drawdown_improvement: float

    verdict: str



class BenchmarkAnalyzer:



    def __init__(

        self,

        starting_cash: float = 100000.0

    ):

        self.starting_cash = starting_cash



    # =====================================================
    # MAIN ANALYSIS
    # =====================================================

    def compare(

        self,

        symbol: str,

        dataframe: pd.DataFrame,

        atlas_results: dict,

    ) -> BenchmarkReport:


        benchmark = self._buy_and_hold(

            dataframe

        )


        atlas_equity = atlas_results.get(

            "ending_equity",

            self.starting_cash

        )


        atlas_return = (

            (

                atlas_equity

                -

                self.starting_cash

            )

            /

            self.starting_cash

        ) * 100



        alpha = (

            atlas_return

            -

            benchmark["return"]

        )



        drawdown_improvement = (

            benchmark["drawdown"]

            -

            atlas_results.get(

                "max_drawdown",

                0

            )

        )



        verdict = self._verdict(

            alpha,

            drawdown_improvement

        )



        return BenchmarkReport(

            symbol=symbol,

            starting_cash=self.starting_cash,

            benchmark_final_equity=benchmark["equity"],

            benchmark_return=benchmark["return"],

            benchmark_drawdown=benchmark["drawdown"],

            atlas_final_equity=atlas_equity,

            atlas_return=atlas_return,

            atlas_drawdown=atlas_results.get(

                "max_drawdown",

                0

            ),

            alpha=alpha,

            drawdown_improvement=drawdown_improvement,

            verdict=verdict,

        )



    # =====================================================
    # BUY AND HOLD
    # =====================================================

    def _buy_and_hold(

        self,

        dataframe

    ):


        prices = dataframe["Close"]



        start = prices.iloc[0]

        end = prices.iloc[-1]



        shares = self.starting_cash / start



        final_equity = shares * end



        return_percent = (

            (

                final_equity

                -

                self.starting_cash

            )

            /

            self.starting_cash

        ) * 100



        drawdown = self._drawdown(

            prices

        )



        return {

            "equity": final_equity,

            "return": return_percent,

            "drawdown": drawdown,

        }



    # =====================================================
    # DRAWDOWN
    # =====================================================

    def _drawdown(

        self,

        prices

    ):


        running_high = prices.cummax()



        drawdowns = (

            (

                prices

                -

                running_high

            )

            /

            running_high

        ) * 100



        return abs(

            drawdowns.min()

        )



    # =====================================================
    # VERDICT
    # =====================================================

    def _verdict(

        self,

        alpha,

        drawdown_improvement

    ):


        score = 0



        if alpha > 0:

            score += 1



        if drawdown_improvement > 0:

            score += 1



        if alpha > 10:

            score += 1



        if score == 3:

            return "OUTPERFORMS"



        if score == 2:

            return "SUPERIOR RISK ADJUSTED"



        if score == 1:

            return "MARGINAL"



        return "UNDERPERFORMS"



# =========================================================
# PRINT REPORT
# =========================================================


def print_benchmark_report(

    report: BenchmarkReport

):


    print()

    print("=" * 60)

    print("ATLAS VS BENCHMARK REPORT")

    print("=" * 60)



    print()

    print(f"Benchmark: {report.symbol}")



    print()

    print("BUY AND HOLD")

    print("-" * 60)

    print(

        f"Final Equity:     ${report.benchmark_final_equity:,.2f}"

    )

    print(

        f"Return:           {report.benchmark_return:.2f}%"

    )

    print(

        f"Max Drawdown:     {report.benchmark_drawdown:.2f}%"

    )



    print()

    print("ATLAS")

    print("-" * 60)

    print(

        f"Final Equity:     ${report.atlas_final_equity:,.2f}"

    )

    print(

        f"Return:           {report.atlas_return:.2f}%"

    )

    print(

        f"Max Drawdown:     {report.atlas_drawdown:.2f}%"

    )



    print()

    print("DIFFERENCE")

    print("-" * 60)

    print(

        f"Alpha:            {report.alpha:.2f}%"

    )

    print(

        f"Drawdown Change:  {report.drawdown_improvement:.2f}%"

    )



    print()

    print(

        f"VERDICT: {report.verdict}"

    )


    print("=" * 60)

    print()