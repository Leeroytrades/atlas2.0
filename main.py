"""
Atlas AI Trading Assistant 2.3

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



    scans = atlas.scan_market()



    trade = atlas.search_and_trade(

        scans

    )



    if trade:

        print()

        print(

            f"Trade created: {trade.symbol}"

        )



    atlas.monitor_trades()



    metrics = atlas.performance()



    current_equity = metrics.get(

        "equity",

        10000.00

    )



    show_dashboard(

        scans=scans,

        portfolio=atlas.portfolio(),

        metrics=metrics,

        equity_history=atlas.equity_history(),

        current_equity=current_equity,

    )


    atlas.close()



if __name__ == "__main__":

    main()