import numpy as np

def add_metrics_to_5min(df_5min):
    df = df_5min.copy()
    df['MA_30min'] = df['Close'].rolling(window=6, min_periods=1).mean()   # 30min ÷ 5min = 6
    df['Median_15min'] = df['Close'].rolling(window=3, min_periods=1).median()  # 15min ÷ 5min = 3
    df['VWAP'] = calculate_vwap(df)
    return df

def add_metrics_to_30min(df_30min):
    df = df_30min.copy()
    # Skip MA/Median - don't make sense for 30-min data
    df['VWAP'] = calculate_vwap(df)
    return df

def calculate_vwap(df):
    # Calculate typical price (HLC/3)
    typical_price = (df['High'] + df['Low'] + df['Close']) / 3
    
    # VWAP = Cumulative(Price * Volume) / Cumulative(Volume)
    vwap = np.cumsum((typical_price * df['Volume'])) / np.cumsum(df['Volume'])
    
    return vwap.round(2)