"""
Atlas AI Trading Assistant 2.0

Portfolio Dashboard Display
"""

from rich.table import Table


def portfolio_table(portfolio):

    table = Table(
        title="Portfolio Overview"
    )

    table.add_column(
        "Metric"
    )

    table.add_column(
        "Value",
        justify="right"
    )


    data = portfolio.summary()


    for key, value in data.items():

        if isinstance(value, float):

            if "Confidence" in key:

                value = f"{value:.0%}"

            else:

                value = f"{value:.2f}"


        table.add_row(
            str(key),
            str(value)
        )


    return table