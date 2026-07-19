"""
Atlas AI Trading Assistant 2.0

Market Scanner Table
"""

from rich.table import Table


def scanner_table(results):

    table = Table(title="Market Scanner")

    table.add_column("Rank", justify="right")
    table.add_column("Symbol")
    table.add_column("Score", justify="right")
    table.add_column("Bias")
    table.add_column("Confidence", justify="right")

    for i, result in enumerate(results, start=1):

        table.add_row(
            str(i),
            result.symbol,
            str(result.score),
            result.bias,
            f"{result.confidence:.0%}",
        )

    return table