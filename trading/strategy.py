import pandas as pd


def analyze_signals(df: pd.DataFrame, short_span: int = 12, long_span: int = 26) -> pd.DataFrame:
    """
    Adds simple EMA crossover signals to a copy of the DataFrame.

    Output columns:
    - ema_short, ema_long: EMAs
    - signal: 1 for buy (short crosses above long), -1 for sell, 0 otherwise

    This is intentionally lightweight for demonstration.
    """
    data = df.copy()
    data['Close'] = data['Close'].astype(float)

    data['ema_short'] = data['Close'].ewm(span=short_span, adjust=False).mean()
    data['ema_long'] = data['Close'].ewm(span=long_span, adjust=False).mean()

    data['signal'] = 0
    # when short EMA crosses above long EMA -> buy (1)
    cross_up = (data['ema_short'] > data['ema_long']) & (data['ema_short'].shift(1) <= data['ema_long'].shift(1))
    cross_down = (data['ema_short'] < data['ema_long']) & (data['ema_short'].shift(1) >= data['ema_long'].shift(1))

    data.loc[cross_up, 'signal'] = 1
    data.loc[cross_down, 'signal'] = -1

    return data
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
