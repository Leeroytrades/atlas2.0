"""
Atlas AI Trading Platform

Performance Service
"""

from __future__ import annotations


class PerformanceService:

    def __init__(
        self,
        metrics,
    ):

        self.metrics = metrics

    def summary(self):

        return self.metrics.calculate()