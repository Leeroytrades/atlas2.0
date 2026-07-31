"""
Atlas AI Trading Platform

Monitoring Service

Runs the complete trading cycle.
"""

from __future__ import annotations



class MonitoringService:


    def __init__(
        self,
        scanner_service,
        execution_service,
        performance_service,
        portfolio_service,
    ):

        self.scanner = scanner_service

        self.execution = execution_service

        self.performance = performance_service

        self.portfolio = portfolio_service



    def run_cycle(self):


        print()

        print(
            "Atlas monitoring cycle..."
        )

        print()



        # Scan markets

        scans = self.scanner.scan()



        # Manage open trades

        closed = self.execution.monitor()



        if closed:

            print(
                "Trades closed:"
            )

            for trade in closed:

                print(
                    trade
                )



        # Update performance

        metrics = self.performance.summary()



        print()

        print(
            "Equity:",
            metrics.get(
                "equity"
            )
        )


        return {

            "scans": scans,

            "closed": closed,

            "metrics": metrics,

        }