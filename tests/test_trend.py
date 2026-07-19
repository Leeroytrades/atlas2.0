"""
Atlas AI Trading Assistant 2.0

Risk Engine Test
"""

from data.market_data import MarketData

from indicators.composite import build_indicator_set

from strategy.signal_generator import generate_scorecard

from risk.risk_manager import create_trade


def main():

    market = MarketData()

    print("\nDownloading AAPL...\n")

    df = market.get_history("AAPL")

    df = build_indicator_set(df)

    score = generate_scorecard(df)

    direction = "LONG"

    if score.bearish:
        direction = "SHORT"

    trade = create_trade(
        symbol="AAPL",
        df=df,
        account_balance=10000,
        risk_percent=1,
        direction=direction,
        confidence=score.confidence,
    )

    print("=" * 70)
    print("ATLAS TRADE PLAN")
    print("=" * 70)

    print(f"Symbol        : {trade.symbol}")
    print(f"Direction     : {trade.direction}")
    print(f"Entry         : {trade.entry:.2f}")
    print(f"Stop Loss     : {trade.stop_loss:.2f}")
    print(f"Take Profit   : {trade.take_profit:.2f}")
    print(f"Quantity      : {trade.quantity}")
    print(f"Risk (£/$)    : {trade.risk_amount:.2f}")
    print(f"Reward        : {trade.reward_amount:.2f}")
    print(f"R:R           : {trade.risk_reward:.2f}")
    print(f"Confidence    : {trade.confidence:.2%}")

    print("=" * 70)


if __name__ == "__main__":
    main()