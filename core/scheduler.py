"""
Atlas AI Trading Platform

Scheduler

Controls timed execution loops
and respects market hours.
"""

from __future__ import annotations


import time

from datetime import datetime


from core.market_hours import MarketHours





class Scheduler:
    """
    Controls repeated Atlas cycles.
    """



    def __init__(
        self,
        interval: int = 60,
        market_hours=None,
    ):

        self.interval = interval

        self.running = False

        self.market_hours = market_hours or MarketHours()



    # ==================================================
    # START LOOP
    # ==================================================

    def start(
        self,
        callback,
    ):

        self.running = True



        print()

        print(
            "Atlas Scheduler Started"
        )

        print(
            f"Interval: {self.interval}s"
        )

        print(
            f"Market Status: {self.market_hours.status()}"
        )

        print()



        while self.running:


            started = datetime.now()



            try:


                if self.market_hours.is_open():


                    callback()


                else:


                    print(

                        "Market closed - waiting..."

                    )



            except Exception as error:


                print()

                print(

                    "Scheduler Error:",

                    error

                )

                print()



            elapsed = (

                datetime.now()

                -

                started

            ).total_seconds()



            wait = max(

                self.interval - elapsed,

                0

            )



            time.sleep(

                wait

            )



    # ==================================================
    # STOP LOOP
    # ==================================================

    def stop(self):

        self.running = False


        print()

        print(

            "Atlas Scheduler Stopped"

        )

        print()