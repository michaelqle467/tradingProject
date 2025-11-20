# tradingProject (fresh scaffold)

This repository contains a minimal Flask-based trading demo that fetches OHLCV data with `yfinance`, applies a simple EMA-crossover trading signal, and visualizes results with Plotly.

This reset provides a clean, runnable scaffold for Windows development.

Quick start (PowerShell)

1. From the repository root (where `app.py` is):

```powershell
python -m venv .venv
# If activation is blocked, allow scripts for current user (one-time):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt

# Run the development server
python app.py
```

2. Alternative: use the provided PowerShell launcher `run.ps1` (after creating the venv once):

```powershell
.\run.ps1
```

3. Production-like server on Windows (optional):

```powershell
pip install waitress
waitress-serve --listen=*:8000 app:app
```

Notes
- `gunicorn` is not supported on native Windows; `waitress` is recommended for local Windows hosting.
- The demo is educational only and not financial advice.

Files of interest
- `app.py` — Flask application
- `trading/strategy.py` — simple EMA crossover signal generator
- `templates/index.html` and `templates/results.html` — UI
- `requirements.txt` — Python dependencies
- `run.ps1` / `run.bat` — convenience start scripts

If you want a different stack or extra features (backtesting, DB, Docker), tell me which direction and I'll scaffold that next.