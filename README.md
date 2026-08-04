Atlas AI Trading Platform
README.md

Version: Atlas 3.5
Project Type: Algorithmic Trading Research Platform
Language: Python 3.12
Environment: Windows 11 + Python Virtual Environment
Status: Active Development

1. Overview

Atlas is an AI-assisted algorithmic trading research platform designed to discover, test, validate, and eventually deploy systematic trading strategies.

The goal of Atlas is not simply to generate buy/sell signals, but to create a complete trading intelligence framework capable of:

Market analysis
Technical indicator processing
Signal generation
Risk management
Historical simulation
Strategy optimisation
Walk-forward validation
Regime detection
Adaptive strategy selection
Portfolio intelligence

Atlas has evolved from a basic trading assistant into a research platform capable of testing whether strategies survive unseen market conditions.

2. Current Version
Atlas 3.5

Current development milestone:

Adaptive Strategy Research Phase

Completed:

✅ Market data engine
✅ Indicator framework
✅ Composite scoring
✅ Signal generation
✅ Risk management
✅ Trade simulation
✅ Portfolio tracking
✅ SQLite persistence
✅ Backtesting engine
✅ Parameter optimisation
✅ Parallel optimisation
✅ Walk-forward validation
✅ Regime detection framework
✅ Trend strategy
✅ Range strategy

Currently developing:

🔄 Adaptive strategy router
🔄 Volatility strategy
🔄 Multi-regime execution engine

3. Core Philosophy

Atlas follows several principles:

3.1 Avoid Overfitting

A strategy that performs perfectly on historical data but fails on unseen data is considered unsuccessful.

Atlas therefore uses:

Training periods
Optimisation
Locked parameters
Unseen validation periods
Walk-forward testing
3.2 Optimise for Robustness

The objective is not maximum profit.

The objective is:

Find strategies that maintain an edge across different market conditions.

Metrics considered:

Profit factor
Drawdown
Win rate
Trade frequency
Stability
Validation performance
3.3 Modular Architecture

Each component is independent.

Example:

Market Data
      |
      v
Indicators
      |
      v
Regime Detection
      |
      v
Strategy Selection
      |
      v
Signal Generation
      |
      v
Risk Management
      |
      v
Execution Simulation
      |
      v
Performance Analysis
4. Current Performance

Latest successful walk-forward validation:

==================================================
ATLAS WALK FORWARD REPORT
==================================================

Total Windows: 5

Passed: 4
Failed: 1

Pass Rate:
80%

Robustness Score:
92/100
Combined Validation Performance
Profit:
209286.64

Trades:
181

Win Rate:
67.4%

Profit Factor:
27.34
Locked Parameters

Current best discovered configuration:

{
    "score_threshold": 40,
    "confidence": 0.4,
    "atr_stop": 4.0,
    "atr_target": 6.0
}
5. Technology Stack
Core
Python 3.12
Data
pandas
numpy
yfinance
Technical Analysis
ta

Indicators include:

EMA
SMA
RSI
MACD
ATR
Bollinger Bands
OBV
CMF
VWAP
ADX
Interface
rich

Used for:

dashboards
reports
console output
Storage
SQLite

Used for:

trades
validation results
research history
6. Installation

Create environment:

python -m venv .venv

Activate:

.venv\Scripts\activate

Install dependencies:

pip install pandas numpy yfinance ta rich pytest pyarrow
7. Running Atlas
Main Application
python main.py
Run Walk Forward Validation
python -m validation.walk_forward
Run Optimisation
python -m optimisation.optimizer
8. Project Structure

Current structure:

Atlas/

│
├── atlas/
│   ├── engine.py
│   ├── session.py
│   ├── portfolio.py
│   └── watchlist.py
│
├── backtesting/
│   ├── engine.py
│   ├── simulator.py
│   ├── historical_data.py
│   └── strategy_runner.py
│
├── data/
│   └── market_data.py
│
├── indicators/
│   ├── composite.py
│   ├── trend.py
│   ├── momentum.py
│   ├── volatility.py
│   └── volume.py
│
├── optimisation/
│   ├── optimizer.py
│   └── parallel_runner.py
│
├── validation/
│   ├── walk_forward.py
│   ├── window.py
│   ├── metrics.py
│   └── report.py
│
├── strategy/
│   ├── signal_generator.py
│   ├── trend_strategy.py
│   ├── range_strategy.py
│   ├── volatility_strategy.py
│   ├── regime_filter.py
│   └── router.py
│
├── risk/
│   ├── risk_manager.py
│   └── trade.py
│
├── database/
│   ├── database.py
│   ├── trades.py
│   └── validation.py
│
└── main.py
9. Current Strategy System

Atlas currently supports:

Trend Strategy

Designed for:

BULLISH
BEARISH
TREND

Uses:

EMA alignment
MACD
RSI
OBV
Range Strategy

Designed for:

SIDEWAYS
RANGE

Uses:

Bollinger Bands
RSI extremes
Volatility compression
Volatility Strategy

Planned.

Purpose:

Handle:

breakout environments
volatility expansion
abnormal market conditions
10. Walk Forward Validation

Atlas validation process:

Historical Data

        |
        v

Split into windows

        |
        v

Training Period

        |
        v

Optimise Parameters

        |
        v

Lock Parameters

        |
        v

Unseen Validation Period

        |
        v

PASS / FAIL

Example:

Training:
1000 candles

Validation:
250 candles
11. Current Known Issue

The adaptive router exists but is not fully connected.

Current flow:

BacktestEngine

      |
      v

StrategyRunner

      |
      v

Signals

Target flow:

BacktestEngine

      |
      v

RegimeDetector

      |
      v

StrategyRouter

      |
      +---- TrendStrategy
      |
      +---- RangeStrategy
      |
      +---- VolatilityStrategy

      |
      v

Signals
12. Development Priorities
Priority 1

Complete StrategyRouter integration.

The system should dynamically choose strategies based on:

regime

Example:

TREND
    -> TrendStrategy

RANGE
    -> RangeStrategy

VOLATILITY
    -> VolatilityStrategy
Priority 2

Complete volatility strategy.

Priority 3

Compare:

Fixed Strategy
vs

Adaptive Router

Using identical walk-forward testing.

Priority 4

Move toward Atlas 4.0:

multi-market support
live market monitoring
alerts
AI explanations
portfolio intelligence
automated research
13. Important Development Rule

When modifying Atlas:

Do not optimise only against training results.

Every change must survive:

Optimisation

+

Walk Forward Validation

+

Unseen Data
14. Current State Summary

Atlas is now beyond a basic trading bot.

Current capability:

Data
 |
Indicators
 |
Signals
 |
Risk
 |
Simulation
 |
Optimisation
 |
Validation
 |
Regime Analysis

The next major milestone is:

Adaptive Intelligence Layer

where Atlas chooses the correct strategy automatically depending on market conditions.