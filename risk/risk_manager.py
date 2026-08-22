"""
Atlas AI Trading Platform 4.2

Risk Manager

Creates trade plans using:

- Account risk
- ATR volatility stops
- Dynamic position sizing
- Reward targets
- Historical entry-price support
- Walk-forward ATR parameters

Designed to remain backwards compatible with the
original Atlas create_trade() interface.
"""

from __future__ import annotations

from models.trade import Trade


# ============================================================
# PRICE
# ============================================================


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


# ============================================================
# ATR
# ============================================================


def get_atr(
    df,
    index=None,
):

    """
    Get ATR value.

    If index is supplied, ATR is taken from that
    historical candle.

    Otherwise the latest ATR is used.

    This is important during backtesting because using
    the latest ATR would introduce look-ahead bias.
    """

    if "ATR" not in df.columns:

        return 0.0

    if index is None:

        value = df["ATR"].iloc[-1]

    else:

        if index < 0 or index >= len(df):

            return 0.0

        value = df["ATR"].iloc[index]

    try:

        atr = float(value)

    except (
        TypeError,
        ValueError,
    ):

        return 0.0

    if atr > 0:

        return atr

    return 0.0


# ============================================================
# POSITION SIZE
# ============================================================


def calculate_position_size(
    account_balance: float,
    risk_percent: float,
    entry: float,
    stop_loss: float,
):

    """
    Calculate position size based on maximum account risk.
    """

    risk_amount = (
        float(account_balance)
        *
        (float(risk_percent) / 100.0)
    )

    distance = abs(
        float(entry)
        -
        float(stop_loss)
    )

    if distance <= 0:

        return 0, risk_amount

    quantity = int(
        risk_amount
        /
        distance
    )

    return quantity, risk_amount


# ============================================================
# CREATE TRADE
# ============================================================


def create_trade(
    symbol: str,
    df=None,
    account_balance: float = 100000.0,
    risk_percent: float = 1.0,
    direction: str | None = None,
    confidence: float = 0.0,
    *,
    entry: float | None = None,
    dataframe=None,
    index: int | None = None,
    atr_stop: float = 2.0,
    atr_target: float = 4.0,
):

    """
    Create a Trade object using ATR volatility.

    Backwards-compatible usage:

        create_trade(
            symbol,
            df,
            account_balance,
            risk_percent,
            direction,
            confidence,
        )

    Backtest usage:

        create_trade(
            symbol=symbol,
            direction="LONG",
            entry=entry_price,
            dataframe=dataframe,
            index=entry_index,
            confidence=confidence,
            atr_stop=2.5,
            atr_target=4.0,
        )

    The explicit historical entry/index interface prevents
    look-ahead bias during backtesting.
    """

    # --------------------------------------------------------
    # DATAFRAME ALIAS
    # --------------------------------------------------------

    if df is None:

        df = dataframe

    if df is None:

        raise ValueError(
            "No dataframe supplied"
        )

    # --------------------------------------------------------
    # DIRECTION
    # --------------------------------------------------------

    if direction is None:

        raise ValueError(
            "Trade direction is required"
        )

    direction = str(
        direction
    ).upper().strip()

    if direction not in (
        "LONG",
        "SHORT",
    ):

        raise ValueError(
            f"Invalid trade direction: {direction}"
        )

    # --------------------------------------------------------
    # ENTRY PRICE
    # --------------------------------------------------------

    if entry is None:

        entry = get_current_price(
            df
        )

    else:

        entry = float(
            entry
        )

    if entry <= 0:

        raise ValueError(
            "Entry price must be positive"
        )

    # --------------------------------------------------------
    # ATR
    #
    # During backtesting use ATR at the entry candle.
    # --------------------------------------------------------

    atr = get_atr(
        df,
        index=index,
    )

    # --------------------------------------------------------
    # ATR FALLBACK
    # --------------------------------------------------------

    if atr <= 0:

        atr = (
            entry
            *
            0.02
        )

    # --------------------------------------------------------
    # STOP / TARGET DISTANCE
    # --------------------------------------------------------

    stop_distance = (
        atr
        *
        float(atr_stop)
    )

    target_distance = (
        atr
        *
        float(atr_target)
    )

    # --------------------------------------------------------
    # LONG
    # --------------------------------------------------------

    if direction == "LONG":

        stop_loss = (
            entry
            -
            stop_distance
        )

        take_profit = (
            entry
            +
            target_distance
        )

    # --------------------------------------------------------
    # SHORT
    # --------------------------------------------------------

    else:

        stop_loss = (
            entry
            +
            stop_distance
        )

        take_profit = (
            entry
            -
            target_distance
        )

    # --------------------------------------------------------
    # POSITION SIZE
    # --------------------------------------------------------

    quantity, risk_amount = (
        calculate_position_size(
            account_balance=account_balance,
            risk_percent=risk_percent,
            entry=entry,
            stop_loss=stop_loss,
        )
    )

    if quantity <= 0:

        return None

    # --------------------------------------------------------
    # REWARD
    # --------------------------------------------------------

    reward_amount = (
        abs(
            take_profit
            -
            entry
        )
        *
        quantity
    )

    # --------------------------------------------------------
    # RISK / REWARD
    # --------------------------------------------------------

    actual_risk = (
        abs(
            entry
            -
            stop_loss
        )
        *
        quantity
    )

    if actual_risk > 0:

        risk_reward = (
            reward_amount
            /
            actual_risk
        )

    else:

        risk_reward = 0.0

    # --------------------------------------------------------
    # CREATE TRADE
    # --------------------------------------------------------

    return Trade(

        symbol=symbol,

        direction=direction,

        entry=entry,

        stop_loss=stop_loss,

        take_profit=take_profit,

        quantity=quantity,

        risk_amount=actual_risk,

        reward_amount=reward_amount,

        risk_reward=round(
            risk_reward,
            2,
        ),

        confidence=float(
            confidence
        ),
    )