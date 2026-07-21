"""
Atlas AI Trading Assistant 2.0

Equity Curve Utilities
"""

from __future__ import annotations



def build_equity_curve(history):

    """
    Convert equity history rows into chart points.
    """

    curve = []


    for row in history:

        try:

            if hasattr(row, "keys"):

                timestamp = row["timestamp"]

                equity = row["equity"]

            else:

                timestamp = row[0]

                equity = row[1]



            if equity is None:

                continue



            curve.append(

                (

                    timestamp,

                    float(equity)

                )

            )


        except Exception:

            continue



    return curve




def calculate_growth(history):

    """
    Calculate growth from equity curve.
    """

    curve = build_equity_curve(history)


    if len(curve) < 2:

        return 0.0



    starting = curve[0][1]

    current = curve[-1][1]



    if starting == 0:

        return 0.0



    return round(

        (

            (

                current - starting

            )

            /

            starting

        )

        *

        100,

        2

    )




def calculate_statistics(history):

    """
    Equity statistics.
    """

    curve = build_equity_curve(history)


    if not curve:

        return {

            "starting": 0,

            "current": 0,

            "growth": 0,

            "points": 0,

        }



    return {

        "starting": curve[0][1],

        "current": curve[-1][1],

        "growth": calculate_growth(history),

        "points": len(curve),

    }