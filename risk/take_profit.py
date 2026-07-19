"""
Take Profit Calculator
"""


def calculate_take_profit(
    entry: float,
    stop: float,
    direction: str,
    rr: float = 2.0,
) -> float:

    risk = abs(entry - stop)

    if direction == "LONG":
        return entry + risk * rr

    return entry - risk * rr