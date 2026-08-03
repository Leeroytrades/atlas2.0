 Atlas AI Trading Platform

## Version

Atlas AI Trading Platform 3.3

Current milestone:

**Research Engine + Optimisation + Walk Forward Validation**

Status:

CORE SYSTEM OPERATIONAL

---

# Project Overview

Atlas is a modular AI-assisted trading research platform built in Python.

The objective is to create a complete trading intelligence system capable of:

- Market data acquisition
- Technical analysis
- Signal generation
- Risk management
- Automated backtesting
- Strategy optimisation
- Walk-forward validation
- Regime detection
- Performance analysis
- Future live trading integration

The architecture is designed around independent modules so individual systems can be upgraded without breaking the platform.

---

# Technology Stack

Python:

3.12

Operating System:

Windows 11

Environment:

.venv virtual environment


Main libraries:

- pandas
- numpy
- yfinance
- ta
- rich
- pytest
- sqlite3


---

# Current Project Status

## Completed Systems

### Market Data Engine

Status:

COMPLETE


Capabilities:

- Historical market data loading
- Cached datasets
- Indicator preparation
- Multi-symbol support


---

## Indicator Engine

Status:

COMPLETE


Includes:

Trend:

- SMA
- EMA
- ADX
- DI+ / DI-


Momentum:

- RSI
- MACD
- Stochastic


Volatility:

- ATR
- Bollinger Bands
- BB Width


Volume:

- OBV
- CMF
- VWAP


---

# Strategy Engine

Status:

COMPLETE


Generates:

- Bull/Bear scores
- Confidence values
- Trade bias
- Signal strength


---

# Risk Management

Status:

COMPLETE


Includes:

- Position sizing
- Risk percentage
- Stop loss calculation
- Take profit calculation
- Risk/reward calculation


Current default:

Account:

$10,000


Risk:

1%


---

# Backtesting Engine

Status:

COMPLETE


Supports:

- Historical simulation
- ATR stops
- ATR targets
- Equity tracking
- Trade statistics


Metrics:

- Profit
- Win rate
- Profit factor
- Drawdown
- Trade count


---

# Database System

Status:

COMPLETE


Database:

atlas.db


Stores:

- Trades
- Portfolio data
- Equity history
- Validation results


---

# Optimisation Engine

Status:

COMPLETE


Location:

optimisation/


Files:


optimizer.py
parallel_runner.py
worker.py
results.py
results_database.py



Capabilities:

- Parameter search
- Parallel optimisation
- Ranking system


Current optimisation parameters:

Score threshold:

40-120


Confidence:

0.4-1.0


ATR Stop:

1.5-4.25


ATR Target:

3.0-6.0


---

# Latest Optimisation Result

Best configuration found:


Profit:

$219,840.94


Ending Equity:

$319,840.94


Starting Capital:

$100,000


Profit Factor:

2.59


Trades:

412


Win Rate:

34.95%


Parameters:


Score threshold: 40

Confidence: 0.4

ATR Stop: 4.25

ATR Target: 5.0



Important:

This is in-sample optimisation only.

Requires validation.


---

# Walk Forward Validation

Status:

IN PROGRESS


Location:

validation/


Purpose:

Prevent overfitting.


Process:

Training Data

↓

Optimisation

↓

Locked Parameters

↓

Unseen Validation

↓

Validation Report


---

# Current Validation Issue

Latest validation result:


PASS:

0 / 10


Problem:

Optimised parameters perform well during training but fail on unseen windows.


Example:

Training:

Profit:
$90,641


Profit Factor:

12.24


Validation:

Trades:

0-19


Profit:

0


or negative


---

# Current Investigation Areas

Possible causes:

1. Strategy overfitting

2. Validation windows too small

3. Regime filter too restrictive

4. Entry logic not generalising

5. Unrealistic optimisation ranking

6. Need stronger robustness scoring


---

# Regime Detection

Status:

COMPLETE


Location:

research/regime_detector.py


Detects:

Trend:

- Bullish
- Bearish
- Sideways


Volatility:

- High
- Normal
- Low


Momentum:

- Positive
- Negative
- Neutral


---

# Current Folder Architecture



Atlas

├── atlas
│ ├── engine.py
│ ├── session.py
│ ├── watchlist.py
│ └── portfolio.py
│
├── data
│ └── market_data.py
│
├── indicators
│ ├── composite.py
│ ├── trend.py
│ ├── momentum.py
│ ├── volatility.py
│ └── volume.py
│
├── strategy
│ └── signal_generator.py
│
├── risk
│ ├── risk_manager.py
│ └── trade.py
│
├── backtesting
│ └── engine.py
│
├── optimisation
│ ├── optimizer.py
│ ├── parallel_runner.py
│ ├── worker.py
│ ├── results.py
│ └── results_database.py
│
├── validation
│ ├── walk_forward.py
│ ├── metrics.py
│ ├── window.py
│ └── report.py
│
├── research
│ ├── regime_detector.py
│ ├── dataset_builder.py
│ ├── benchmark.py
│ └── score_builder.py
│
├── database
│ ├── database.py
│ ├── trades.py
│ ├── portfolio.py
│ ├── equity.py
│ └── validation.py
│
└── main.py


---

# Important Commands


Activate environment:


.venv\Scripts\activate



Run Atlas:


python main.py



Run optimisation:


python -m optimisation.optimizer



Run validation:


python -m validation.walk_forward



Check git:


git status



View commits:


git log --oneline -5



---

# Git Status

Current branch:


refactor/atlas-2.1



Latest commit:


93884c0 Atlas 3.3 complete - optimisation and walk forward validation



---

# Next Development Priority

## Phase 1

Fix Walk Forward Validation


Goals:

- Improve out-of-sample performance
- Reduce overfitting
- Add robustness scoring
- Test multiple markets


---

## Phase 2

Strategy Improvements

Potential additions:

- Market regime dependent parameters
- Adaptive thresholds
- Multiple timeframe confirmation
- Better entry filtering


---

## Phase 3

Production Features

Future:

- Live market monitoring
- Alerts
- AI trade explanations
- Portfolio dashboard
- Broker integration


---

# Developer Notes

The user prefers:

- Complete file replacements rather than patches
- Clear copy/paste solutions
- Minimal unnecessary explanations during coding
- Preserve working architecture
- Avoid breaking existing modules


---

END OF STATUS DOCUMENT