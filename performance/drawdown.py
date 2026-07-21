"""
Atlas AI Trading Platform

Drawdown Calculator

Tracks:
- Peak equity
- Current drawdown
- Maximum drawdown
"""

from __future__ import annotations



class DrawdownCalculator:


    def __init__(self):

        self.peak_equity = 0.0

        self.current_drawdown = 0.0

        self.maximum_drawdown = 0.0



    def update(
        self,
        equity: float,
    ):

        """
        Update drawdown from new equity value.
        """


        if equity > self.peak_equity:

            self.peak_equity = equity



        if self.peak_equity == 0:

            self.current_drawdown = 0

            return



        self.current_drawdown = (

            (

                self.peak_equity

                -

                equity

            )

            /

            self.peak_equity

        ) * 100



        if self.current_drawdown > self.maximum_drawdown:

            self.maximum_drawdown = self.current_drawdown



    def summary(
        self,
    ) -> dict:

        return {

            "peak_equity": round(
                self.peak_equity,
                2
            ),

            "current_drawdown": round(
                self.current_drawdown,
                2
            ),

            "maximum_drawdown": round(
                self.maximum_drawdown,
                2
            ),

        }