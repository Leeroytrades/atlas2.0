Atlas AI Trading Assistant 3.0
Project Status

Date:
31 July 2026

Current State

Atlas is currently operational.

The system can:

✅ Load market data
✅ Generate technical indicators
✅ Produce trading signals
✅ Create trades
✅ Manage risk
✅ Track portfolio state
✅ Store trades in SQLite
✅ Simulate historical trades
✅ Run optimisation experiments

Current Milestone
Backtesting + Optimisation Phase

Status:

IN PROGRESS

Latest Completed Work
StrategyRunner

Completed.

Now supports:

Score threshold filtering
Confidence filtering
Configurable optimisation parameters

Verified:

Score threshold changes signal quantity:

50 = 102 signals
60 = 98 signals
70 = 92 signals
80 = 78 signals
100 = 29 signals
120 = 6 signals

Confidence filtering verified:

0.5 = 92 signals
0.6 = 92 signals
0.7 = 92 signals
0.8 = 78 signals
0.9 = 54 signals
1.0 = 29 signals
Optimiser Status

Current file:

optimisation/optimizer.py

Current search:

768 combinations.

Parameters:

Score
Confidence
ATR Stop
ATR Target

Currently running:

python optimise.py SPY

Allow completion.

Current Backtest Findings

SPY baseline:

Starting Cash:
100000

Ending Equity:
97343.44

Net Profit:
-2656.56

Trades:
61

Wins:
23

Losses:
38

Win Rate:
37.7%

Profit Factor:
0.83

Current conclusion:

The optimisation framework was not the issue.

The strategy itself needs improvement.

Important Discoveries

The Atlas scoring engine is heavily bullish.

Example signals:

110 1.0 BUY
130 1.0 BUY
130 1.0 BUY
80  0.8 BUY
90  0.9 BUY

Future improvement areas:

Short selling logic
Market regime filtering
Trend/range detection
Better entry confirmation
Next Development Steps
Step 1

Finish current optimiser run.

Review:

Best configuration
Profit factor
Win rate
Trade count
Step 2

Save winning configuration:

Example:

config/
    optimized_strategy.json

Atlas live engine loads this automatically.

Step 3

Improve strategy engine:

Add:

Long/short symmetry
Market regime filter
Volatility filter
Volume confirmation
Step 4

Multi-market testing

Test:

SPY
QQQ
AAPL
MSFT
NVDA
AMD
META
Step 5

Paper trading validation

Before broker integration:

Run live paper mode
Track performance
Compare against backtest
User Workflow Preference

Important:

When changing Atlas:

Always provide:

✅ complete replacement files
✅ not partial snippets
✅ include exact filename
✅ include testing command afterwards

Backup

GitHub repository:

Leeroytrades/atlas2.0

Before stopping work:

git add .
git commit -m "Atlas milestone update"
git push
Resume Instructions

When continuing:

Check:

Optimiser result
PROJECT_STATUS.md
README.md

Then continue from:

"Strategy improvement and adaptive optimisation."
What I recommend next

I wouldn't spend any more time tuning the current optimiser until we implement these improvements:

✅ Download historical data only once.
✅ Cache the data to disk.
✅ Make the optimiser reuse the same dataframe.
✅ Add multiprocessing so all CPU cores work simultaneously.
✅ Save every optimisation run to a CSV/SQLite database so the best settings are remembered permanently.

After that, Atlas won't need to repeat hundreds of identical downloads, and you'll build up a historical library of optimisation results instead of recomputing them every time.