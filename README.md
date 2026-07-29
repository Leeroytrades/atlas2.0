# Atlas AI Trading Assistant 3.0

Professional modular algorithmic trading platform built in Python.

Atlas is designed as a complete trading research and execution framework:

- Market data ingestion
- Technical analysis
- AI-style scoring engine
- Risk management
- Backtesting
- Market selection
- Portfolio tracking
- Trade database
- Dashboard
- Paper trading preparation
- Broker integration ready architecture

---

# Current Version

Atlas AI Trading Assistant 3.0

Status:

🟢 Core architecture complete  
🟢 Backtesting operational  
🟢 Multi-market testing operational  
🟢 Market ranking operational  
🟢 Dynamic watchlist operational  
🟡 Paper trading preparation in progress  
🔴 Live trading not enabled

---

# Project Architecture


Atlas2.0

│
├── atlas/
│ ├── engine.py
│ ├── session.py
│ ├── scanner.py
│ └── watchlist.py
│
├── backtesting/
│ ├── engine.py
│ ├── simulator.py
│ ├── strategy_runner.py
│ ├── historical_data.py
│ ├── reports.py
│ ├── multi_engine.py
│ ├── analytics.py
│ └── atlas_strategy.py
│
├── data/
│ └── market_data.py
│
├── indicators/
│ ├── composite.py
│ ├── trend.py
│ ├── momentum.py
│ ├── volatility.py
│ └── volume.py
│
├── scoring/
│ ├── trend_score.py
│ ├── momentum_score.py
│ ├── volatility_score.py
│ └── volume_score.py
│
├── strategy/
│ └── signal_generator.py
│
├── risk/
│ ├── risk_manager.py
│ ├── position_manager.py
│ └── trade_monitor.py
│
├── services/
│ ├── execution_service.py
│ ├── performance_service.py
│ ├── portfolio_service.py
│ ├── scanner_service.py
│ ├── strategy_service.py
│ └── trade_service.py
│
├── database/
│ ├── database.py
│ ├── trades.py
│ ├── equity_history.py
│ └── journal.py
│
├── watchlist/
│ └── market_selector.py
│
├── display/
│ └── dashboard.py
│
└── main.py


---

# Core System Flow


Market Data

  ↓

Indicators

  ↓

Scoring Engine

  ↓

Signal Generator

  ↓

Risk Manager

  ↓

Trade Creation

  ↓

Database

  ↓

Portfolio

  ↓

Dashboard


---

# Completed Features

## Market Scanner

Completed.

Features:

- Multiple symbol scanning
- Indicator generation
- Scorecard creation
- BUY / SELL / HOLD classification


---

## Technical Indicators

Completed.

Current indicators:

- SMA 20
- SMA 50
- EMA 20
- EMA 50
- ADX
- DI+
- DI-
- RSI
- ATR
- Bollinger Width
- Volume metrics


---

## Scoring Engine

Completed.

Components:

Trend Score

Momentum Score

Volatility Score

Volume Score


Example:


Trend: 40
Momentum: 20
Volatility: 10
Volume: 20

Total: 90
Signal: BUY


---

# Risk Management

Completed.

Current:

- Account risk calculation
- Position sizing
- Stop placement
- Take profit
- Risk reward calculation


---

# Backtesting System

Completed.

Capabilities:

- Historical data loading
- Strategy execution
- Trade simulation
- ATR stop loss
- ATR take profit
- Trailing stops
- Maximum holding period
- Slippage
- Commission simulation
- Equity tracking


---

# Backtesting Results

Latest multi-market testing:

## MSFT


Profit:
+2907

Trades:
6

Win Rate:
50%

Profit Factor:
2.69


---

## AAPL


Profit:
+1461

Trades:
8

Win Rate:
50%

Profit Factor:
1.56


---

## QQQ


Profit:
+791

Trades:
23

Win Rate:
43.48%

Profit Factor:
1.15


---

## SPY

Currently filtered:


Loss:
-3320

Profit Factor:
0.80


---

Combined:


Markets Tested:
5

Trades:
99

Wins:
40

Combined Profit:
+1838

Win Rate:
40.4%


---

# Market Selection

Completed.

Process:


Backtest Results

    ↓

Market Analytics

    ↓

Ranking

    ↓

Market Selector

    ↓

watchlist.txt


Current selected watchlist example:


MSFT
QQQ
AAPL


---

# Database

Completed.

SQLite persistence.

Current tables:

Trades

Stores:

- Symbol
- Direction
- Entry
- Stop
- Target
- Quantity
- Risk
- Reward
- Confidence
- Status
- Profit/Loss


Equity history

Trade journal


---

# Services Layer

Created.

Current services:


execution_service.py

performance_service.py

portfolio_service.py

scanner_service.py

strategy_service.py

trade_service.py


---

# Current Development Phase

## Phase 4: Paper Trading Preparation

Next objectives:

1. Connect market selector to live scanning

2. Create paper execution engine

3. Add trade lifecycle management

4. Add signal explanations

5. Add portfolio risk controls

6. Improve dashboard

---

# Important Development Rule

DO NOT replace random individual files.

Future changes should be:

1. Identify module
2. Replace complete file
3. Test
4. Commit to GitHub


---

# Environment

Windows 11

Python:

3.12.10

Virtual environment:


.venv


Run:


.venv\Scripts\activate
python main.py


---

# Git Repository

Repository:

https://github.com/Leeroytrades/atlas2.0


Backup:


git add .
git commit -m "Update Atlas"
git push origin main


---

# Current Goal

Transform Atlas from:

"Backtesting research platform"

into:

"Paper trading AI trading assistant"

Next milestone:

ATLAS LIVE ENGINE 3.1