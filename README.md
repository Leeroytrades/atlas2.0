# Atlas AI Trading Assistant 2.0

## Overview

Atlas AI Trading Assistant 2.0 is a modular AI-assisted trading platform designed to analyse markets, generate trade ideas, manage risk, track positions, and provide performance analytics.

The project has evolved from a market scanner into a structured trading engine.

---

# Current Features

## Market Scanner

Atlas scans a configurable watchlist and ranks symbols using a composite scoring system.

Features:

- Symbol scanning
- Market ranking
- Bullish/bearish bias detection
- Confidence scoring
- Trade opportunity identification

Example:


AAPL

Score: 70
Bias: BUY
Confidence: 70%


---

## Technical Analysis Engine

Atlas processes historical market data through an indicator pipeline.

Current analysis areas:

- Trend
- Momentum
- Volatility
- Volume

Pipeline:


Market Data
|
v
Indicators
|
v
Scorecard
|
v
Trading Signal


---

# Strategy Engine

The strategy engine converts market analysis into trading decisions.

Outputs:

- Direction
- Confidence
- Bias
- Trade eligibility

Example:


Direction:
LONG

Confidence:
70%


---

# Risk Management

Atlas includes a complete risk calculation system.

Features:

- Entry calculation
- Stop loss calculation
- Take profit calculation
- Position sizing
- Risk amount
- Reward amount
- Risk/reward ratio

Example:


Entry:
328.20

Stop:
311.80

Target:
361.00

Risk:
$100

Reward:
$197

Risk Reward:
1.97


---

# Trade Management

Trade objects support:

- Symbol
- Direction
- Entry
- Stop loss
- Take profit
- Quantity
- Risk
- Reward
- Confidence
- Status
- Open timestamp
- Close timestamp
- Exit price
- Profit/Loss


Trade lifecycle:


SIGNAL GENERATED

    |

    v

OPEN TRADE

    |

    v

MONITOR POSITION

    |

    v

TARGET OR STOP HIT

    |

    v

CLOSED TRADE


---

# Portfolio System

Atlas tracks:

- Account balance
- Active positions
- Exposure
- Open trades

Duplicate protection prevents multiple open positions on the same symbol.

Example:


Existing position detected for AAPL

Trade creation skipped.


---

# Database System

Atlas uses SQLite persistence.

Database:


atlas.db


Stores:

- Trades
- Positions
- Status
- Entry prices
- Stop loss
- Take profit
- Confidence
- Timestamps
- Exit information
- Profit/Loss

---

# Execution Engine

The execution layer monitors active trades.

Current capabilities:

- Load open trades
- Monitor positions
- Detect stop loss
- Detect take profit
- Close trade foundation
- Calculate realised P/L foundation

---

# Performance Analytics

Atlas performance system calculates:

- Total trades
- Closed trades
- Wins
- Losses
- Win rate
- Total profit/loss
- Average win
- Average loss
- Profit factor

Future additions:

- Equity curve
- Drawdown tracking
- Monthly returns
- Advanced statistics

---

# Dashboard

Atlas uses the Rich terminal interface.

Current dashboard sections:

- Market Scanner
- Atlas Scorecard
- Trade Plan
- Portfolio
- Performance Metrics

---

# Project Structure


Atlas2.0

├── atlas
│ ├── engine.py
│ ├── session.py
│ └── scanner.py
│
├── data
│ └── market_data.py
│
├── indicators
│ └── composite.py
│
├── strategy
│ └── signal_generator.py
│
├── risk
│ ├── risk_manager.py
│ └── position_manager.py
│
├── database
│ ├── database.py
│ ├── trades.py
│ ├── portfolio.py
│ └── journal.py
│
├── execution
│ └── manager.py
│
├── performance
│ ├── metrics.py
│ └── statistics.py
│
├── display
│ ├── dashboard.py
│ ├── tables.py
│ └── performance.py
│
├── main.py
│
└── atlas.db


---

# Running Atlas

Activate environment:


.venv\Scripts\activate


Run:


python -m main


---

# Development Philosophy

Atlas is built around:

- Modular architecture
- Clear separation of systems
- Expandable components
- Database persistence
- Production-style organisation

---

# Future Development

## Equity Curve System

Will add:

- Account growth tracking
- Drawdown monitoring
- Returns analysis


## Backtesting Engine

Will add:

- Historical simulation
- Strategy testing
- Performance comparison


## Live Market Monitor

Will add:

- Real-time pricing
- Alerts
- Automated monitoring


---

# Current Status

Atlas AI Trading Assistant 2.0 has a stable core engine and is ready for advanced analytics, testing, and expansion.