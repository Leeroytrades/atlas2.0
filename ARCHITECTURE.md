Atlas AI Trading Platform
System Architecture Document

Version: Atlas 3.x
Purpose: Quantitative trading research, optimisation, backtesting and live trading foundation

1. Project Overview

Atlas is a modular AI-assisted quantitative trading platform designed to:

Collect market data
Generate technical indicators
Produce multi-factor trading signals
Backtest historical strategies
Optimise strategy parameters
Validate strategies on unseen data
Manage risk
Track trades
Prepare for future live trading integration

The project has evolved from a simple trading assistant into a research platform capable of:

Strategy discovery
Parameter optimisation
Walk-forward validation
Quantitative ranking
Portfolio management
Broker integration readiness
2. Core Design Philosophy

Atlas follows these principles:

Modular Architecture

Each component has a single responsibility.

Example:

Market Data
|
v
Indicators
|
v
Scoring Engines
|
v
Signal Generator
|
v
Backtesting Engine
|
v
Optimisation Engine
|
v
Validation

Research First

No strategy should be trusted from a single backtest.

The workflow is:

Train on historical data
Optimise parameters
Validate on unseen data
Reject overfitted results
Only then consider live deployment
Risk Before Reward

A profitable strategy is not enough.

Atlas evaluates:

Profit
Win rate
Profit factor
Trade frequency
Drawdown
Stability
3. Current Project Structure
Atlas/

│
├── main.py
├── optimise.py
├── validate.py
│
├── atlas/
│   ├── engine.py
│   ├── session.py
│   ├── watchlist.py
│   └── portfolio.py
│
├── data/
│   ├── market_data.py
│   └── cache/
│
├── indicators/
│   └── composite.py
│
├── scoring/
│   ├── trend_score.py
│   ├── momentum_score.py
│   ├── volatility_score.py
│   └── volume_score.py
│
├── strategy/
│   ├── signal_generator.py
│
├── backtesting/
│   ├── engine.py
│   ├── strategy_runner.py
│   ├── simulator.py
│   └── historical_data.py
│
├── optimisation/
│   ├── optimizer.py
│   ├── parallel_runner.py
│   ├── results_database.py
│   └── configurations.py
│
├── research/
│   └── dataset_cache.py
│
├── risk/
│   └── risk_manager.py
│
├── models/
│   ├── trade.py
│   └── scorecard.py
│
├── database/
│   ├── database.py
│   └── trades.py
│
└── display/
    └── dashboard.py
4. Data Pipeline
Market Data Layer

Location:

data/market_data.py

Responsibilities:

Download historical market data
Normalise dataframe structure
Provide OHLCV data

Current development source:

Yahoo Finance through yfinance

Required dataframe columns:

Open
High
Low
Close
Volume
5. Dataset Cache System

Location:

research/dataset_cache.py

Purpose:

Avoid repeatedly downloading and calculating indicators.

Workflow:

Market Data

     |

Indicator Builder

     |

Parquet Dataset Cache

     |

Backtesting / Optimisation

Cached datasets currently support:

SPY
Historical periods
Multiple intervals

Example:

data/cache/SPY_2y_1d.parquet
6. Indicator System

Location:

indicators/composite.py

Responsible for building technical indicators.

Current indicators:

Trend
EMA20
EMA50
SMA20
SMA50
ADX
DI+
DI-
Momentum
RSI
MACD
MACD Signal
Stochastic
Volume
OBV
CMF
VWAP
Volatility
ATR
7. Scoring Architecture

Location:

scoring/

Atlas uses independent scoring engines.

Trend Score

File:

trend_score.py

Evaluates:

EMA alignment
SMA alignment
Price position
ADX strength
Directional movement

Maximum contribution:

70 points

Momentum Score

File:

momentum_score.py

Evaluates:

RSI
MACD
Stochastic
Volume Score

File:

volume_score.py

Evaluates:

OBV trend
Money flow
VWAP position
Volatility Score

File:

volatility_score.py

Evaluates:

ATR conditions
Market movement suitability
8. Signal Generator

Location:

strategy/signal_generator.py

Purpose:

Convert indicator scores into trading decisions.

Output:

BUY
SELL
HOLD

Signal confirmation currently uses:

Total score threshold
ADX confirmation
RSI filter
Volume confirmation
Volatility confirmation
EMA20 pullback filter
9. Scorecard Model

Location:

models/scorecard.py

Stores:

trend
momentum
volatility
volume

total_score

signal

confidence

Confidence:

abs(total_score) / 100
10. Backtesting Engine

Location:

backtesting/
Backtest Engine

Responsible for:

Running historical strategies
Creating trades
Simulating exits
Returning performance
11. Strategy Runner

Location:

backtesting/strategy_runner.py

Responsibilities:

Walk through historical candles
Generate rolling indicators
Create historical signals
Apply optimisation thresholds

Important:

The runner was improved to avoid rebuilding unnecessary calculations.

Current architecture:

Historical Candle

       |

Rolling Window

       |

Signal Generator

       |

Trade Signal
12. Trade Simulator

Location:

backtesting/simulator.py

Current features:

Long trades
Short trades
ATR stop loss
ATR targets
Breakeven protection
Maximum holding period
Commission
Slippage
Equity tracking

Current optimisation discovery:

Strong results are appearing around:

ATR Stop:
3.5 - 4.25

ATR Target:
5.0 - 5.5
13. Optimisation Engine

Location:

optimisation/

Purpose:

Automatically search strategy parameters.

Current parameters tested:

Score threshold

Example:

40
50
60
70
Confidence

Example:

0.4
0.5
0.6
ATR Stop

Example:

3.0
3.5
4.0
4.25
ATR Target

Example:

4.0
4.5
5.0
5.5
14. Current Optimisation Results

Latest research:

Dataset:

SPY
2514 rows

Best discovered configuration:

Score:
40

Confidence:
0.4

ATR Stop:
4.0

ATR Target:
5.5

Performance:

Profit:
$185,056.99

Win Rate:
40.81%

Profit Factor:
3.89

Other strong configurations:

ATR 3.75 / 5.5

ATR 4.25 / 5.5
15. Validation System

Purpose:

Prevent overfitting.

Workflow:

Training Data

        |

Optimisation

        |

Best Parameters

        |

Unseen Validation Data

        |

PASS / FAIL

Important:

Earlier validation failures showed:

High training profit does not guarantee robustness.

Future improvements required:

Walk forward testing
Multiple symbols
Market regime testing
Monte Carlo testing
16. Risk Management

Location:

risk/

Responsibilities:

Position sizing
Stop placement
Risk percentage calculation

Future:

Portfolio exposure
Correlation management
Volatility based sizing
17. Database System

Location:

database/

SQLite currently stores:

Trades:

symbol
direction
entry
stop_loss
take_profit
quantity
risk
reward
confidence
status
profit_loss

Optimisation database stores:

Parameters
Results
Rankings
18. Current Development Stage

Completed:

YES

Market data
Indicator system
Scoring engine
Signal generator
Backtesting
Simulator
Optimisation
Dataset caching
SQLite storage

Currently working on:

Robust validation
Preventing overfitting
Strategy selection
Live trading preparation
19. Immediate Next Development Priorities

Priority 1:

Improve validation

Add:

Walk forward testing
Multiple market periods
Multiple symbols

Priority 2:

Improve ranking model

Include:

Drawdown
Stability
Sharpe ratio
Sortino ratio

Priority 3:

Create production strategy profile

Example:

ATLAS_PRODUCTION_PROFILE

Score:
40

Confidence:
0.5

ATR:
4.0 / 5.5

Priority 4:

Prepare live trading layer

Possible integrations:

Interactive Brokers
Alpaca
Tradovate
NinjaTrader
20. Important Development Notes

When modifying Atlas:

Always provide complete replacement files
Avoid partial snippets
Maintain modular structure
Do not remove working functionality
Test after each major change
Preserve cached datasets

Current objective:

Create a professional quantitative trading platform capable of discovering, validating and deploying robust strategies.

END ARCHITECTURE DOCUMENT