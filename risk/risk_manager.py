"""
Atlas AI Trading Assistant 2.0

Risk Manager
"""

from __future__ import annotations

import pandas as pd

from risk.trade import Trade
from risk.position_sizer import calculate_position_size
from risk.stop_loss import calculate_stop_loss
from risk.take_profit import calculate_take_profit


def create_trade(
    symbol: str,
    df: pd.DataFrame,
    account_balance: float,
    risk_percent: float,
    direction: str,
    confidence: float,
) -> Trade:
    """
    Build a complete trade plan.
    """

    latest = df.iloc[-1]

    entry = float(latest["Close"])

    stop_loss = calculate_stop_loss(
        df=df,
        direction=direction,
    )

    take_profit = calculate_take_profit(
        entry=entry,
        stop=stop_loss,
        direction=direction,
        rr=2.0,
    )

    quantity = calculate_position_size(
        account_balance=account_balance,
        risk_percent=risk_percent,
        entry_price=entry,
        stop_price=stop_loss,
    )

    risk_amount = abs(entry - stop_loss) * quantity
    reward_amount = abs(take_profit - entry) * quantity

    risk_reward = 0.0

    if risk_amount > 0:
        risk_reward = reward_amount / risk_amount

    return Trade(
        symbol=symbol,
        direction=direction,
        entry=entry,
        stop_loss=stop_loss,
        take_profit=take_profit,
        quantity=quantity,
        risk_amount=risk_amount,
        reward_amount=reward_amount,
        risk_reward=risk_reward,
        confidence=confidence,
    )