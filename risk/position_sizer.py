"""
Position Sizing
"""

from math import floor


def calculate_position_size(
    account_balance: float,
    risk_percent: float,
    entry_price: float,
    stop_price: float,
) -> int:

    risk_amount = account_balance * (risk_percent / 100)

    risk_per_share = abs(entry_price - stop_price)

    if risk_per_share <= 0:
        return 0

    quantity = floor(risk_amount / risk_per_share)

    return max(quantity, 0)