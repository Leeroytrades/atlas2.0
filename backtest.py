"""
Atlas AI Trading Platform 3.0

Backtest Runner

Standalone command:

python backtest.py SPY
"""

from __future__ import annotations


import sys


from backtesting.engine import BacktestEngine



def main():


    if len(sys.argv) < 2:

        print()

        print(
            "Usage: python backtest.py SYMBOL"
        )

        print()

        print(
            "Example: python backtest.py SPY"
        )

        print()

        return



    symbol = sys.argv[1].upper()



    print()

    print(
        "================================="
    )

    print(
        " Atlas Backtest"
    )

    print(
        " Symbol:",
        symbol
    )

    print(
        "================================="
    )

    print()



    engine = BacktestEngine()



    results = engine.run(

        symbol

    )



    print()

    print(
        "Backtest Results"
    )

    print(
        "----------------"
    )



    for key, value in results.items():

        print(
            f"{key}: {value}"
        )



    print()



if __name__ == "__main__":

    main()