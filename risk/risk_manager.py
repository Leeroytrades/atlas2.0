"""
Atlas AI Trading Assistant 2.3.4

Risk Manager

Creates trade plans using:

- Account risk
- ATR volatility stops
- Dynamic position sizing
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



def get_atr(df):

    """
    Get latest ATR value.
    """

    if "ATR" in df.columns:

        atr = float(
            df["ATR"].iloc[-1]
        )

        if atr > 0:

            return atr


    return 0



def calculate_position_size(
    account_balance: float,
    risk_percent: float,
    entry: float,
    stop_loss: float,
):

    """
    Calculate position size based on risk.
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
    Create a Trade object using ATR volatility.
    """

    entry = get_current_price(
        df
    )


    atr = get_atr(
        df
    )


    #
    # ATR fallback protection
    #

    if atr == 0:

        atr = entry * 0.02



    if direction == "LONG":


        stop_loss = entry - (

            atr * 2

        )


        take_profit = entry + (

            atr * 4

        )


    else:


        stop_loss = entry + (

            atr * 2

        )


        take_profit = entry - (

            atr * 4

        )



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