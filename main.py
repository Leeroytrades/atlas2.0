"""
Atlas AI Trading Platform 3.0

Application Entry Point
"""

from __future__ import annotations


from atlas.engine import AtlasEngine

from display.dashboard import show_dashboard



def main():


    atlas = AtlasEngine()



    print()

    print("Scanning Market...")

    print()



    # -----------------------------
    # Scan Market
    # -----------------------------

    scans = atlas.scan_market()



    # -----------------------------
    # Find Trade
    # -----------------------------

    trade = atlas.search_and_trade(
        scans
    )


    if trade:

        print()

        print(
            f"Paper trade opened: {trade.symbol}"
        )



    # -----------------------------
    # Monitor Open Trades
    # -----------------------------

    atlas.monitor_trades()



    # -----------------------------
    # Performance
    # -----------------------------

    metrics = atlas.performance()



    # -----------------------------
    # Equity History
    # -----------------------------

    equity_history = atlas.equity_history()



    # -----------------------------
    # Dashboard
    # -----------------------------

    show_dashboard(

        scans=scans,

        portfolio=atlas.portfolio(),

        metrics=metrics,

        equity_history=equity_history,

        current_equity=metrics.get(

            "equity",

            10000.0

        ),

    )



    atlas.close()



if __name__ == "__main__":

    main()