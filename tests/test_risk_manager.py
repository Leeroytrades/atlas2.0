"""
Atlas AI Trading Assistant 3.0

Risk Manager Tests
"""

import pandas as pd

from risk.risk_manager import create_trade



def test_create_long_trade():

    df = pd.DataFrame(
        {
            "Close": [
                100,
                101,
                102,
            ],
            "ATR": [
                2,
                2,
                2,
            ],
        }
    )


    trade = create_trade(

        symbol="TEST",

        df=df,

        account_balance=10000,

        risk_percent=1,

        direction="LONG",

        confidence=0.80,

    )


    assert trade is not None

    assert trade.symbol == "TEST"

    assert trade.direction == "LONG"

    assert trade.entry == 102

    assert trade.stop_loss < trade.entry

    assert trade.take_profit > trade.entry

    assert trade.quantity > 0



def test_create_short_trade():

    df = pd.DataFrame(
        {
            "Close": [
                100,
                101,
                102,
            ],
            "ATR": [
                2,
                2,
                2,
            ],
        }
    )


    trade = create_trade(

        symbol="TEST",

        df=df,

        account_balance=10000,

        risk_percent=1,

        direction="SHORT",

        confidence=0.75,

    )


    assert trade is not None

    assert trade.direction == "SHORT"

    assert trade.stop_loss > trade.entry

    assert trade.take_profit < trade.entry