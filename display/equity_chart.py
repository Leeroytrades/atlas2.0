"""
Atlas AI Trading Platform

Terminal Equity Chart
"""

from __future__ import annotations


from rich.console import Group

from rich.text import Text



def equity_chart(
    values: list[float]
):


    if not values:

        return Text(
            "No equity history available"
        )



    highest = max(values)

    lowest = min(values)



    if highest == lowest:

        return Text(
            f"Equity: ${highest:,.2f}"
        )



    chart = []

    height = 10



    for level in range(
        height,
        0,
        -1
    ):


        threshold = (

            lowest

            +

            (

                highest - lowest

            )

            *

            level

            /

            height

        )


        line = ""


        for value in values:


            if value >= threshold:

                line += "●"

            else:

                line += " "



        chart.append(

            Text(line)

        )



    chart.append(

        Text(

            f"\n${lowest:,.2f}"

            +

            " " * 5

            +

            f"${highest:,.2f}"

        )

    )


    return Group(

        *chart

    )