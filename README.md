# TradingProject

A simple Python web app (Flask) that fetches historical price data (via yfinance), runs a basic trading strategy (EMA crossover with RSI filter), and visualizes buy/sell signals on an interactive Plotly candlestick chart.

Features
- Enter a ticker symbol and timeframe on the website
- Fetch historical OHLCV using yfinance
- Strategy: EMA crossover (short vs long) with RSI confirmation
- Interactive Plotly chart that marks buy and sell signals
- Table of detected buy/sell signals and basic position performance

How to run locally

1. Prerequisites
   - Python 3.10 or later
   - Git (if you plan to clone/push)
   - (Optional) Virtual environment tool (venv)

2. Clone the repo (if not already):
   git clone https://github.com/michaelqle467/tradingProject.git
   cd tradingProject

3. Create and activate a virtual environment
   # Linux / macOS
   python -m venv venv
   source venv/bin/activate

   # Windows (PowerShell)
   python -m venv venv
   .\\venv\\Scripts\\Activate.ps1

   # Windows (cmd.exe)
   python -m venv venv
   venv\\Scripts\\activate

4. Install dependencies
   pip install -r requirements.txt

5. Run the app
   # Option A: direct run (development)
   python app.py
   # or, with Flask env var:
   export FLASK_APP=app.py       # macOS/Linux
   set FLASK_APP=app.py          # Windows (cmd)
   flask run

   The app will be available at http://127.0.0.1:5000/

6. Usage
   - Open the web UI.
   - Enter a ticker symbol (e.g., AAPL or BTC-USD), choose a history period and interval, then click Analyze.
   - The app fetches historical data, runs the EMA crossover + RSI filter strategy, and displays buy/sell markers on a Plotly candlestick chart along with a signals table.

Notes & next steps
- This is an educational example and not financial advice. Backtest thoroughly before using real capital.
- You can extend the project by adding:
  - A backtesting engine to compute returns, drawdowns, and performance metrics
  - Storage (database) to save queries and results
  - Additional indicators and strategy parameters exposed via the UI
  - Integration with broker APIs for paper/live trading (requires API keys)
  - Deployment instructions (Docker, Gunicorn, hosting)

License
- Add your preferred license file if you want this code to be open source (e.g., MIT).