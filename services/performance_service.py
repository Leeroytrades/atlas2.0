"""
Atlas AI Trading Platform

Performance Service

Connects performance calculations
to the application layer.
"""

from __future__ import annotations

from performance.metrics import PerformanceMetrics


class PerformanceService:
    """
    Handles performance analytics.
    """

    def __init__(
        self,
        trade_repository,
    ):

        self.metrics = PerformanceMetrics(
            trade_repository
        )


    def summary(self):
        """
        Return complete performance data.
        """

        metrics = self.metrics.calculate()


        # Ensure required dashboard fields exist

        if "equity" not in metrics:

            metrics["equity"] = (

                metrics.get(
                    "starting_balance",
                    10000.00
                )

                +

                metrics.get(
                    "net_profit",
                    0.0
                )

            )


        if "growth" not in metrics:

            starting = metrics.get(
                "starting_balance",
                10000.00
            )


            if starting:

                metrics["growth"] = round(

                    (

                        (
                            metrics["equity"]
                            -
                            starting
                        )

                        /

                        starting

                    )

                    *

                    100,

                    2

                )

            else:

                metrics["growth"] = 0.0


        return metrics