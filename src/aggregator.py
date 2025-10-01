def aggregate_ohlc(df_1min, timeframe):
    """
    Aggregate 1-minute OHLC data to specified timeframe
    
    Args:
        df_1min: 1-minute OHLC DataFrame
        timeframe: Aggregation period ('5min', '30min', '1D')
    
    Returns:
        Aggregated OHLC DataFrame
    """
    if len(df_1min) == 0:
        raise ValueError("Cannot aggregate empty DataFrame")
    
    # Group by time interval and calculate OHLC
    aggregated = df_1min.resample(timeframe).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    })
    
    return aggregated

# Specific aggregation functions
def aggregate_to_5min(df_1min):
    return aggregate_ohlc(df_1min, '5min')

def aggregate_to_30min(df_1min):
    return aggregate_ohlc(df_1min, '30min')

def aggregate_to_1d(df_1min):
    return aggregate_ohlc(df_1min, '1D')