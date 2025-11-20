from flask import Flask, render_template, jsonify
import yfinance as yf
import time
from pathlib import Path


app = Flask(__name__)


def load_sp100_tickers():
    path = Path(__file__).parent / 'data' / 'sp100.txt'
    if not path.exists():
        return []
    with open(path, 'r', encoding='utf-8') as f:
        ticks = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return ticks


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/top100')
def api_top100():
    """Return JSON for S&P 100 tickers: symbol, name, price, prev_close, pct_change, marketCap"""
    tickers = load_sp100_tickers()
    results = []
    start = time.time()
    for sym in tickers:
        try:
            t = yf.Ticker(sym)
            info = t.info or {}
            hist = t.history(period='2d')
            if hist is None or hist.empty:
                continue
            # get last close and previous close if available
            closes = hist['Close'].tolist()
            if len(closes) == 1:
                last = closes[-1]
                prev = closes[-1]
            else:
                prev = closes[-2]
                last = closes[-1]

            pct = None
            try:
                pct = ((last - prev) / prev) * 100 if prev != 0 else None
            except Exception:
                pct = None

            market_cap = info.get('marketCap')
            name = info.get('shortName') or info.get('longName') or ''

            results.append({
                'symbol': sym,
                'name': name,
                'price': float(last) if last is not None else None,
                'prev_close': float(prev) if prev is not None else None,
                'pct_change': float(pct) if pct is not None else None,
                'market_cap': int(market_cap) if market_cap is not None else None,
            })
        except Exception:
            # keep going on errors for individual tickers
            continue
    # sort by market cap descending (None => 0)
    results.sort(key=lambda r: r['market_cap'] or 0, reverse=True)
    # limit to top 100 just in case
    elapsed = time.time() - start
    return jsonify({'generated_at': int(time.time()), 'elapsed_seconds': elapsed, 'data': results[:100]})


if __name__ == '__main__':
    app.run(debug=True)
