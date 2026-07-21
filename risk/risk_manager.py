"""
Atlas AI Trading Platform

Risk Manager

Creates trade plans using:

- Account risk
- Position sizing
- Stop placement
- Reward targets
"""

from __future__ import annotations

from models.trade import Trade



def get_current_price(df):

    """
    Extract latest closing price.
    """

    possible_columns = [

        "Close",

        "close",

        "Adj Close",

        "adj_close",

    ]


    for column in possible_columns:

        if column in df.columns:

            return float(
                df[column].iloc[-1]
            )


    raise ValueError(
        "No closing price column found"
    )



def calculate_position_size(
    account_balance: float,
    risk_percent: float,
    entry: float,
    stop_loss: float,
):

    """
    Calculate trade quantity based on risk.
    """

    risk_amount = (

        account_balance

        *
        (risk_percent / 100)

    )


    distance = abs(
        entry - stop_loss
    )


    if distance == 0:

        return 0, risk_amount


    quantity = int(

        risk_amount

        /
        distance

    )


    return quantity, risk_amount



def create_trade(
    symbol: str,
    df,
    account_balance: float,
    risk_percent: float,
    direction: str,
    confidence: float,
):

    """
    Create a new Trade object.
    """

    entry = get_current_price(
        df
    )


    if direction == "LONG":

        stop_loss = entry * 0.95

        take_profit = entry * 1.10


    else:

        stop_loss = entry * 1.05

        take_profit = entry * 0.90



    quantity, risk_amount = calculate_position_size(

        account_balance,

        risk_percent,

        entry,

        stop_loss,

    )


    if quantity <= 0:

        return None



    reward_amount = abs(

        take_profit - entry

    ) * quantity



    risk_reward = (

        reward_amount / risk_amount

        if risk_amount > 0

        else 0

    )


    return Trade(

        symbol=symbol,

        direction=direction,

        entry=entry,

        stop_loss=stop_loss,

        take_profit=take_profit,

        quantity=quantity,

        risk_amount=risk_amount,

        reward_amount=reward_amount,

        risk_reward=round(
            risk_reward,
            2
        ),

        confidence=confidence,

    )