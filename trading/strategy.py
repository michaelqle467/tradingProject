import pandas as pd
import numpy as np

def ema(series: pd.Series, span: int):
    return series.ewm(span=span, adjust=False).mean()

def compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ma_up = up.ewm(span=period, adjust=False).mean()
    ma_down = down.ewm(span=period, adjust=False).mean()
    rs = ma_up / (ma_down + 1e-10)
    rsi = 100 - (100 / (1 + rs))
    return rsi

def analyze_signals(df: pd.DataFrame,
                    ema_short_period: int = 12,
                    ema_long_period: int = 26,
                    rsi_period: int = 14,
                    rsi_buy_threshold: int = 30,
                    rsi_sell_threshold: int = 70) -> pd.DataFrame:
    """
    Adds columns to df:
      - ema_short, ema_long, rsi
      - signal: 1 for buy, -1 for sell, 0 for hold
    Strategy:
      - Buy when ema_short crosses above ema_long AND rsi < rsi_sell_threshold (avoid overbought)
      - Sell when ema_short crosses below ema_long AND rsi > rsi_buy_threshold (avoid oversold)
    """

    close = df['Close']
    df['ema_short'] = ema(close, ema_short_period)
    df['ema_long'] = ema(close, ema_long_period)
    df['rsi'] = compute_rsi(close, rsi_period)

    df['ema_diff'] = df['ema_short'] - df['ema_long']
    df['ema_diff_prev'] = df['ema_diff'].shift(1)

    # crossover detection
    df['signal'] = 0
    buy_mask = (df['ema_diff'] > 0) & (df['ema_diff_prev'] <= 0) & (df['rsi'] < rsi_sell_threshold)
    sell_mask = (df['ema_diff'] < 0) & (df['ema_diff_prev'] >= 0) & (df['rsi'] > rsi_buy_threshold)

    df.loc[buy_mask, 'signal'] = 1
    df.loc[sell_mask, 'signal'] = -1

    # attach metadata for plotting labels
    df.attrs['ema_short_period'] = ema_short_period
    df.attrs['ema_long_period'] = ema_long_period

    # clean helper columns
    df.drop(columns=['ema_diff', 'ema_diff_prev'], inplace=True)

    return df
