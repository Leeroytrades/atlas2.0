"""
Atlas AI Trading Platform

Scheduler

Controls timed execution loops.
"""

from __future__ import annotations

import time
from datetime import datetime



class Scheduler:
    """
    Simple application scheduler.
    """


    def __init__(
        self,
        interval: int = 60,
    ):

        self.interval = interval

        self.running = False



    def start(
        self,
        callback,
    ):

        self.running = True


        while self.running:


            started = datetime.now()


            callback()



            elapsed = (

                datetime.now()

                -

                started

            ).seconds



            wait = max(

                self.interval - elapsed,

                0

            )


            time.sleep(
                wait
            )



    def stop(self):

        self.running = False