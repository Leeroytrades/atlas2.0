"""
Atlas AI Trading Platform 3.0

Optimisation Runner

Usage:

python optimise.py SYMBOL

Example:

python optimise.py SPY
"""

from __future__ import annotations

import sys

from optimisation.optimizer import StrategyOptimizer



def main():


    if len(sys.argv) < 2:

        print()

        print(
            "Usage: python optimise.py SYMBOL"
        )

        print()

        print(
            "Example: python optimise.py SPY"
        )

        print()

        return



    symbol = sys.argv[1].upper()



    print()

    print(
        "================================="
    )

    print(
        " Atlas Strategy Optimiser"
    )

    print(
        f" Symbol: {symbol}"
    )

    print(
        "================================="
    )

    print()



    optimizer = StrategyOptimizer(
        symbol
    )



    results = optimizer.optimise()



    print()

    print(
        "Best Configurations"
    )

    print(
        "------------------"
    )



    if not results:

        print(
            "No optimisation results produced."
        )

        return



    for index, result in enumerate(

        results[:10],

        start=1,

    ):


        print()



        print(

            f"{index}. "

            f"Profit ${result['net_profit']:.2f} | "

            f"Win Rate {result['win_rate']:.2f}% | "

            f"PF {result['profit_factor']}"

        )



        print(

            "   "

            f"Score {result['score_threshold']} | "

            f"Confidence {result['confidence']} | "

            f"ATR {result['atr_stop']}/{result['atr_target']}"

        )



        print(

            f"   Ranking Score: "

            f"{result['ranking_score']}"

        )



    print()



if __name__ == "__main__":

    main()