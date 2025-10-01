import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_1min_ohlc(start_price, seed):
    """
    Generate 1-minute OHLC data for a single trading day (9:30 AM - 4:00 PM)
    
    Args:
        start_price: Initial price at market open
        seed: Random seed for reproducibility
    
    Returns:
        DataFrame with OHLC data and random volume
    """
    trading_minutes = 390  # 6.5h * 60min 
    np.random.seed(seed)
    
    # Generate main price path 
    returns = np.random.normal(0, 0.0005, trading_minutes) # Use random percentage changes
    returns[0] = 0  # No change at open

    # cumsum() used for performance over loops
    prices = start_price * (1 + np.cumsum(returns)) 
    
    timestamps = []
    ohlc_data = []
    
    current_time = datetime.now().replace(hour=9, minute=30, second=0, microsecond=0)
    
    for i in range(trading_minutes):
        timestamp = current_time + timedelta(minutes=i)
        timestamps.append(timestamp)
        
        # For each minute, generate OHLC within the minute
        minute_open = prices[i]
        minute_returns = np.random.normal(0, 0.0002, 5)  # 5 changes per minute
        minute_prices = minute_open * (1 + np.cumsum(minute_returns))

        ohlc_data.append({
            'Open': round(minute_prices[0], 2),
            'High': round(max(minute_prices), 2),
            'Low': round(min(minute_prices), 2),
            'Close': round(minute_prices[-1], 2),
            'Volume': np.random.randint(1000, 10000) # Random volume for VWAP
        })
    
    df = pd.DataFrame(ohlc_data, pd.DatetimeIndex(timestamps))
    df.index.name = 'Timestamp'
    
    return df

