"""
Atlas AI Trading Assistant 2.0

Performance Service

Connects performance calculations
to the application layer.
"""

from __future__ import annotations


from performance.metrics import PerformanceMetrics



class PerformanceService:


    def __init__(
        self,
        trade_repository
    ):

        self.metrics = PerformanceMetrics(

            trade_repository

        )



    def summary(self):

        return self.metrics.calculate()