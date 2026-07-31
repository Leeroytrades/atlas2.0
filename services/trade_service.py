"""
Atlas AI Trading Platform 3.0

Trade Service

Creates trades using:

- Strategy signals
- Market data
- Risk configuration
- Position sizing
"""

from __future__ import annotations


from datetime import datetime


from models.trade import Trade


from core.config import Config





class TradeService:


    def __init__(self):

        pass



    # ==================================================
    # CREATE TRADE
    # ==================================================

    def create(
        self,
        symbol: str,
        df,
        score,
        account_balance: float | None = None,
    ):


        if df is None or df.empty:

            return None



        account = (

            account_balance

            if account_balance is not None

            else Config.ACCOUNT_SIZE

        )



        price = float(

            df["Close"].iloc[-1]

        )



        atr = float(

            df["ATR"].iloc[-1]

        )



        if score.bias == "BUY":

            direction = "LONG"

            stop_loss = price - atr

            take_profit = price + (atr * 2)



        else:

            direction = "SHORT"

            stop_loss = price + atr

            take_profit = price - (atr * 2)



        risk_per_share = abs(

            price - stop_loss

        )



        if risk_per_share <= 0:

            return None



        max_risk = (

            account

            *

            Config.RISK_PERCENT

            /

            100

        )



        quantity = int(

            max_risk

            /

            risk_per_share

        )



        if quantity < 1:

            quantity = 1



        risk_amount = (

            risk_per_share

            *

            quantity

        )



        reward_amount = (

            abs(

                take_profit - price

            )

            *

            quantity

        )



        risk_reward = 0



        if risk_amount > 0:

            risk_reward = round(

                reward_amount

                /

                risk_amount,

                2

            )



        trade = Trade(

            symbol=symbol,

            direction=direction,

            entry=price,

            stop_loss=stop_loss,

            take_profit=take_profit,

            quantity=quantity,

            risk_amount=round(

                risk_amount,

                2

            ),

            reward_amount=round(

                reward_amount,

                2

            ),

            risk_reward=risk_reward,

            confidence=score.confidence,

            opened=datetime.now(),

        )



        return trade