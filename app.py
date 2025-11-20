from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import yfinance as yf
from trading.strategy import analyze_signals
import plotly.graph_objs as go
from plotly.offline import plot
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    symbol = request.form.get('symbol', 'AAPL').upper().strip()
    period = request.form.get('period', '6mo')  # e.g., '1mo','3mo','6mo','1y','2y'
    interval = request.form.get('interval', '1d')  # '1d', '1h', etc.

    # Fetch data
    try:
        df = yf.download(symbol, period=period, interval=interval, progress=False)
    except Exception as e:
        return render_template('index.html', error=f"Error fetching data for {symbol}: {e}")

    if df.empty:
        return render_template('index.html', error=f"No data found for {symbol}")

    df.dropna(inplace=True)
    df.index = pd.to_datetime(df.index)

    # Analyze
    results = analyze_signals(df.copy())

    # Build Plotly candlestick chart with buy/sell markers
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=results.index,
        open=results['Open'],
        high=results['High'],
        low=results['Low'],
        close=results['Close'],
        name='Price'
    ))

    # Add EMAs
    if 'ema_short' in results.columns and 'ema_long' in results.columns:
        fig.add_trace(go.Scatter(x=results.index, y=results['ema_short'], mode='lines', name=f"EMA {results.attrs.get('ema_short_period', '')}", line=dict(width=1)))
        fig.add_trace(go.Scatter(x=results.index, y=results['ema_long'], mode='lines', name=f"EMA {results.attrs.get('ema_long_period', '')}", line=dict(width=1)))

    # Buy markers
    buys = results[results['signal'] == 1]
    sells = results[results['signal'] == -1]

    if not buys.empty:
        fig.add_trace(go.Scatter(
            x=buys.index,
            y=buys['Low'] * 0.995,
            mode='markers',
            marker=dict(symbol='triangle-up', color='green', size=12),
            name='Buy'
        ))

    if not sells.empty:
        fig.add_trace(go.Scatter(
            x=sells.index,
            y=sells['High'] * 1.005,
            mode='markers',
            marker=dict(symbol='triangle-down', color='red', size=12),
            name='Sell'
        ))

    fig.update_layout(xaxis_rangeslider_visible=False, title=f"{symbol} — Buy/Sell Signals")

    plot_div = plot(fig, include_plotlyjs=False, output_type='div')

    # Format signals table
    signal_rows = []
    for idx, row in results[results['signal'] != 0].iterrows():
        signal_rows.append({
            'date': idx.strftime('%Y-%m-%d %H:%M:%S') if isinstance(idx, pd.Timestamp) else str(idx),
            'signal': 'BUY' if row['signal'] == 1 else 'SELL',
            'price': float(row['Close'])
        })

    return render_template('results.html', symbol=symbol, plot_div=plot_div, signals=signal_rows, period=period, interval=interval)

if __name__ == '__main__':
    app.run(debug=True)
