"""
Atlas AI Trading Platform 3.1

Application Entry Point

Modes:

Normal:
    python main.py

Live monitoring:
    python main.py --live
"""

from __future__ import annotations


import sys


from atlas.engine import AtlasEngine

from core.scheduler import Scheduler

from display.dashboard import show_dashboard



def run_once(
    atlas: AtlasEngine,
):

    print()

    print(
        "Scanning Market..."
    )

    print()



    scans = atlas.scan_market()



    trade = atlas.search_and_trade(
        scans
    )


    if trade:

        print()

        print(
            f"Paper trade opened: {trade.symbol}"
        )



    atlas.monitor_trades()



    metrics = atlas.performance()



    show_dashboard(

        scans=scans,

        portfolio=atlas.portfolio(),

        metrics=metrics,

        equity_history=atlas.equity_history(),

        current_equity=metrics.get(

            "equity",

            10000.0

        ),

    )



def run_live(
    atlas: AtlasEngine,
):

    print()

    print(
        "ATLAS LIVE MODE STARTED"
    )

    print(
        "Monitoring markets..."
    )

    print()



    scheduler = Scheduler(

        interval=300

    )


    try:

        scheduler.start(

            lambda:

            run_once(
                atlas
            )

        )


    except KeyboardInterrupt:


        print()

        print(
            "Stopping Atlas..."
        )


        scheduler.stop()



def main():


    atlas = AtlasEngine()



    try:


        if "--live" in sys.argv:


            run_live(
                atlas
            )


        else:


            run_once(
                atlas
            )


    finally:


        atlas.close()



if __name__ == "__main__":

    main()