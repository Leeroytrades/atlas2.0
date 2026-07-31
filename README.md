Atlas AI Trading Assistant 3.0
Overview

Atlas AI Trading Assistant is a modular algorithmic trading research platform designed for:

Market scanning
Technical analysis
Signal generation
Risk management
Paper trading
Trade monitoring
Performance analytics
Historical backtesting
Strategy optimisation

The project is built in Python with a clean modular architecture designed to evolve toward professional-grade trading infrastructure.

Current Version
Atlas 3.0

Current development focus:

Backtesting engine
Strategy optimisation
Multi-market analysis
Automated configuration discovery
Technology Stack
Language

Python 3.12

Environment

Windows 11

Virtual environment:

.venv
Main Libraries
pandas
numpy
yfinance
ta
rich
pytest
Project Architecture
Atlas2.0/

│
├── main.py
├── backtest.py
├── optimise.py
│
├── atlas/
│   ├── engine.py
│   ├── session.py
│   ├── portfolio.py
│   └── watchlist.py
│
├── data/
│   └── market_data.py
│
├── indicators/
│   └── composite.py
│
├── strategy/
│   └── signal_generator.py
│
├── risk/
│   ├── risk_manager.py
│   └── trade.py
│
├── services/
│   ├── scanner_service.py
│   ├── trade_service.py
│   ├── paper_trading_service.py
│   ├── execution_service.py
│   ├── monitoring_service.py
│   └── performance_service.py
│
├── database/
│   ├── database.py
│   └── trades.py
│
├── backtesting/
│   ├── engine.py
│   ├── simulator.py
│   ├── strategy_runner.py
│   ├── historical_data.py
│   ├── analytics.py
│   ├── reports.py
│   └── multi_engine.py
│
└── optimisation/
    └── optimizer.py
Completed Features
Market Intelligence

Completed:

Market data retrieval
Indicator generation
Composite scoring
Bull/bear bias detection
Confidence scoring
Trading System

Completed:

Trade model
Position sizing
Risk calculations
Stop loss handling
Take profit handling
Portfolio tracking
Paper trading workflow
Database

Completed:

SQLite persistence.

Tracks:

Symbol
Direction
Entry
Stop loss
Take profit
Quantity
Risk
Reward
Confidence
Open/closed status
Profit/loss
Dashboard

Completed:

Rich terminal dashboard showing:

Market scanner
Portfolio
Performance analytics
Equity statistics
Backtesting System

Completed:

Historical simulation engine.

Features:

Historical candle replay
Signal generation
Trade lifecycle simulation
ATR stops
ATR targets
Trailing stops
Commission simulation
Slippage simulation
Equity tracking
Strategy Optimisation

Current development:

Atlas Optimiser.

Current search:

Score Threshold:
50-120

Confidence:
0.5-1.0

ATR Stop:
1.5-3.0

ATR Target:
3.0-6.0

Total combinations:

768

The optimiser ranks configurations using:

Profit
Profit factor
Win rate
Trade reliability
Current Development Goal

Transform Atlas from a functional trading framework into an adaptive strategy research platform.

Next priorities:

Complete optimisation system
Save winning configurations
Multi-symbol optimisation
Market regime detection
Strategy improvement
Live paper trading validation
Broker integration readiness
Development Rules

When modifying Atlas:

Keep modules independent
Use complete replacement files
Avoid partial patches
Test after each milestone
Commit working versions to GitHub