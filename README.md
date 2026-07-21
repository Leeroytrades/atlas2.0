# Atlas AI Trading Assistant 2.1

## Overview

Atlas AI Trading Assistant is a modular Python trading platform designed for professional-style market analysis, risk management, trade tracking, and future broker integration.

The project is built with a clean architecture allowing new features to be added without rebuilding the core system.

Current focus:

- Market scanning
- Technical analysis
- Signal scoring
- Risk management
- Portfolio tracking
- Trade database
- Performance analytics
- Trade journal
- Equity tracking
- Trade monitoring


---

# Current Version

## Atlas AI Trading Assistant 2.1


Status:

✅ Core engine operational  
✅ Database persistence operational  
✅ Scanner operational  
✅ Portfolio system operational  
✅ Performance analytics operational  
✅ Equity history operational  
✅ Trade journal operational  
✅ Trade monitoring operational  


---

# Architecture


main.py

|
v

AtlasEngine

|
+----------------+
|                |

Session Database
| |
| +--> Trades
| +--> Journal
| +--> Equity History
| +--> Portfolio
|
+--> Watchlist
|
+--> Scanner
|
+--> Risk Management
|
+--> Trade Monitor
|
+--> Performance Engine



---

# Project Structure


Atlas2.0/

│
├── main.py
├── README.md
├── PROJECT_STATUS.md
├── watchlist.txt
├── atlas.db
│
├── atlas/
│ ├── engine.py
│ ├── session.py
│ ├── scanner.py
│ └── watchlist.py
│
├── database/
│ ├── database.py
│ ├── trades.py
│ ├── journal.py
│ ├── equity_history.py
│ ├── portfolio.py
│ └── models.py
│
├── performance/
│ ├── metrics.py
│ └── equity_chart.py
│
├── risk/
│ ├── position_manager.py
│ ├── trade_monitor.py
│ └── trade_state.py
│
├── services/
│ └── performance_service.py
│
├── display/
│ ├── dashboard.py
│ ├── panels.py
│ ├── tables.py
│ └── equity.py
│
├── indicators/
│
├── strategy/
│
└── models/



---

# Current Features

## Market Scanner

- Dynamic watchlist support
- Symbol scanning
- Technical indicator analysis
- Score generation
- Bull/Bear bias


## Strategy Engine

Current scoring includes:

- Trend
- Momentum
- Volatility
- Volume


Example:


AAPL
Score: 70
Bias: BUY
Confidence: 70%



---

# Risk Management

Implemented:

- Position manager
- Risk calculations
- Stop loss handling
- Take profit handling
- Trade state tracking


---

# Database

SQLite database:


atlas.db



Current tables:


trades

portfolio

journal

equity_history



Trades store:

- Symbol
- Direction
- Entry
- Stop Loss
- Take Profit
- Quantity
- Risk
- Reward
- Confidence
- Status
- Exit price
- Profit/Loss


---

# Performance System

Tracks:

- Total trades
- Open trades
- Closed trades
- Wins
- Losses
- Win rate
- Net profit
- Equity
- Growth
- Drawdown
- Expectancy


---

# Trade Journal

Records:

- Trade events
- Signals
- Scores
- Confidence
- Market conditions
- Outcomes


---

# Running Atlas

Activate environment:


.venv\Scripts\activate



Run:


python main.py



---

# Git Backup

Check status:


git status



Save changes:


git add .

git commit -m "Atlas update"

git push



---

# Next Development Phase

## Atlas 2.2

Planned:

- Automatic trade execution
- Signal → Trade creation pipeline
- Broker integration layer
- Backtesting engine
- AI trade explanations
- Live market monitoring
- Alerts
- Advanced portfolio analytics


---

# Developer

Liam Thornton

Atlas AI Trading Assistant