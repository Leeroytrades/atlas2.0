"""
Atlas AI Trading Platform 3.0

Multi Market Backtest Runner

Runs Atlas strategy across the watchlist
and ranks historical performance.
"""

from __future__ import annotations


from backtesting.multi_engine import MultiBacktestEngine

from backtesting.analytics import MarketAnalytics



WATCHLIST = [

    "SPY",
    "QQQ",
    "AAPL",
    "MSFT",
    "NVDA",
    "AMD",
    "META",
    "AMZN",
    "GOOG",
    "TSLA",

]





def main():


    print()

    print(
        "================================="
    )

    print(
        " Atlas Multi Market Backtest"
    )

    print(
        "================================="
    )

    print()



    engine = MultiBacktestEngine()



    results = engine.run(

        WATCHLIST

    )



    print()

    print(
        "Analysing Results..."
    )

    print()



    analytics = MarketAnalytics(

        results

    )


    rankings = analytics.rank_markets()



    print()

    print(
        "Market Rankings"
    )

    print(
        "----------------"
    )



    for index, market in enumerate(

        rankings,

        start=1

    ):


        print(

            f"{index}. "

            f"{market['symbol']} | "

            f"Score {market['score']} | "

            f"Profit ${market['profit']} | "

            f"Win Rate {market['win_rate']}% | "

            f"Trades {market['trades']}"

        )



    print()



if __name__ == "__main__":

    main()