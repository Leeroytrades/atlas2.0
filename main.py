"""
Atlas AI Trading Platform 3.0

Application Entry Point
"""

from __future__ import annotations


from atlas.engine import AtlasEngine


from core.scheduler import Scheduler

from core.market_hours import MarketHours

from core.config import Config


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

            Config.ACCOUNT_SIZE

        ),

    )





def main():


    atlas = AtlasEngine()



    market_hours = MarketHours()



    scheduler = Scheduler(

        interval=Config.SCHEDULER_INTERVAL,

        market_hours=market_hours,

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



    finally:


        scheduler.stop()


        atlas.close()





if __name__ == "__main__":

    main()