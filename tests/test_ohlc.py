import pytest
import pandas as pd
import numpy as np
from src.data_generator import generate_1min_ohlc
from src.aggregator import aggregate_to_5min, aggregate_to_30min, aggregate_to_1d
from src.metrics import add_metrics_to_5min, calculate_vwap

class TestOHLCGeneration:    
    def test_ohlc_relationship(self):
        """Test OHLC relationships"""
        df = generate_1min_ohlc(100.0, 42)
        
        # High must be >= Open, Close, Low
        assert all(df['High'] >= df['Open'])
        assert all(df['High'] >= df['Close']) 
        assert all(df['High'] >= df['Low'])
        
        # Low must be <= Open, Close, High  
        assert all(df['Low'] <= df['Open'])
        assert all(df['Low'] <= df['Close'])
        assert all(df['Low'] <= df['High'])

    def test_timestamp_structure(self):
        """Test that output has proper datetime index structure"""
        df = generate_1min_ohlc(100.0, 42)
        
        assert isinstance(df.index, pd.DatetimeIndex)
        assert df.index.name == 'Timestamp'
        assert len(df) == 390 
        
        assert df.index[0].hour == 9 and df.index[0].minute == 30
        
        expected_end = df.index[0] + pd.Timedelta(minutes=389) 
        assert df.index[-1] == expected_end
    
    def test_price_positive(self):
        """Test that all prices are positive"""
        df = generate_1min_ohlc(100.0, 42)
        assert all(df[['Open', 'High', 'Low', 'Close']] > 0)
    
    def test_reproducibility(self):
        """Test that same seed produces same results"""
        seeds = [42, 123, 456]  # Test multiple seeds
        
        for seed in seeds:
            df1 = generate_1min_ohlc(100.0, seed)
            df2 = generate_1min_ohlc(100.0, seed)
            df3 = generate_1min_ohlc(100.0, seed + 1) 
            
            pd.testing.assert_frame_equal(df1, df2)
            
            with pytest.raises(AssertionError):
                pd.testing.assert_frame_equal(df1, df3)

class TestAggregation:
    @pytest.mark.parametrize("timeframe,expected_bars,agg_func", [
        ('5min', 78, aggregate_to_5min),
        ('30min', 13, aggregate_to_30min),  
        ('1D', 1, aggregate_to_1d),
    ])
    def test_aggregation_timeframes(self, timeframe, expected_bars, agg_func):
        """Test all aggregation timeframes"""
        df_1min = generate_1min_ohlc(100.0, 42)
        result = agg_func(df_1min)
        
        assert len(result) == expected_bars
        
        if timeframe == '5min':
            first_period = df_1min.iloc[:5]
        elif timeframe == '30min':
            first_period = df_1min.iloc[:30]
        elif timeframe == '1D':
            first_period = df_1min.iloc[:] 
        else:
            raise ValueError(f"Unsupported timeframe: {timeframe}")
        
        assert result.iloc[0]['Open'] == first_period.iloc[0]['Open']
        assert result.iloc[0]['High'] == first_period['High'].max()
        assert result.iloc[0]['Low'] == first_period['Low'].min()
        assert result.iloc[0]['Close'] == first_period.iloc[-1]['Close']

    def test_time_index_requirements(self):
        """Test that aggregation requires DateTimeIndex"""
        df_no_timeindex = pd.DataFrame({
            'Open': [100, 101], 'High': [102, 103], 'Low': [99, 100],
            'Close': [101, 102], 'Volume': [1000, 2000]
        })
        # Regular index, not DateTimeIndex
        
        with pytest.raises(Exception):  
            aggregate_to_5min(df_no_timeindex)

    def test_empty_dataframe(self):
        """Test handling of empty input data"""
        empty_df = pd.DataFrame(
            columns=['Open', 'High', 'Low', 'Close', 'Volume'],
            index=pd.DatetimeIndex([])
        )
        with pytest.raises(ValueError):
            aggregate_to_5min(empty_df)

    def test_single_row(self):
        """Test aggregation with single row of data"""
        single_row = pd.DataFrame({
            'Open': [100], 'High': [102], 'Low': [98], 
            'Close': [101], 'Volume': [1000]
        }, index=pd.DatetimeIndex([pd.Timestamp('2024-01-01 09:30:00')]))
        
        result = aggregate_to_5min(single_row)
        assert len(result) == 1
        # Verify the single row becomes the aggregated bar
        assert result.iloc[0]['Open'] == 100
        assert result.iloc[0]['High'] == 102
        assert result.iloc[0]['Low'] == 98
        assert result.iloc[0]['Close'] == 101
        assert result.iloc[0]['Volume'] == 1000

    def test_missing_columns(self):
        """Test error handling for missing columns"""
        df_missing = pd.DataFrame({
            'Open': [100], 'High': [102]  
        }, index=pd.DatetimeIndex([pd.Timestamp('2024-01-01 09:30:00')]))
        
        with pytest.raises(KeyError):
            aggregate_to_5min(df_missing)
    
    def test_volume(self):
        """Test volume is summed correctly"""
        df_1min = generate_1min_ohlc(100.0, 42)
        df_5min = aggregate_to_5min(df_1min)
        
        first_5min_volume = df_1min.iloc[:5]['Volume'].sum()
        assert df_5min.iloc[0]['Volume'] == first_5min_volume

class TestMetrics:
    def test_vwap_calculation(self):
        """Test VWAP calculation"""
        df = pd.DataFrame({
            'Open': [100, 101],
            'High': [102, 103], 
            'Low': [99, 100],
            'Close': [101, 102],
            'Volume': [1000, 2000]
        })
        
        vwap = calculate_vwap(df)
        typical_price1 = (102 + 99 + 101) / 3
        typical_price2 = (103 + 100 + 102) / 3
        expected_vwap1 = typical_price1
        expected_vwap2 = (typical_price1*1000 + typical_price2*2000) / 3000
        
        assert abs(vwap[0] - expected_vwap1) < 0.01 
        assert abs(vwap[1] - expected_vwap2) < 0.01 
    
    def test_metrics(self):
        """Test metrics calculation"""
        df_5min = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104, 105],
            'High': [102, 103, 104, 105, 106, 107],
            'Low': [99, 100, 101, 102, 103, 104],
            'Close': [101, 102, 103, 104, 105, 106],
            'Volume': [1000, 2000, 3000, 4000, 5000, 6000]
        })
        df_with_ma = add_metrics_to_5min(df_5min)
        assert 'MA_30min' in df_with_ma.columns
        assert 'Median_15min' in df_with_ma.columns
        assert 'VWAP' in df_with_ma.columns

        # Test specific calculations 
        assert len(df_with_ma['MA_30min']) == 6 # 30min ÷ 5min = 6
        assert len(df_with_ma['Median_15min']) == 6 # 15min ÷ 5min = 3

    def test_metrics_insufficient(self):
        """Test metrics with insufficient data"""
        df_short = pd.DataFrame({
            'Open': [100], 'High': [102], 'Low': [98], 
            'Close': [101], 'Volume': [1000]
        })
        result = add_metrics_to_5min(df_short)
        assert not pd.isna(result['MA_30min'].iloc[0])
        assert not pd.isna(result['Median_15min'].iloc[0]) 

if __name__ == "__main__":
    pytest.main()