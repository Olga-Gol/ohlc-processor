# OHLC Data Aggregation and Analysis Tool

A Python tool for generating synthetic OHLC price data and aggregating it to multiple timeframes with technical indicators and interactive charts.

## Features

- Generate realistic 1-minute OHLC data for trading days
- Aggregate to 5-minute, 30-minute, and 1-day timeframes
- Calculate technical indicators (VWAP, moving average, moving median)
- Visualization with timeframe switching
- Test coverage

## Requirements

- pandas
- numpy
- plotly
- pytest

## Quick Start

git clone <repository-url>
cd ohlc-aggregator

### Install dependencies
pip install -r requirements.txt

### Run the complete example
python main.py

## Testing

pytest tests/
#### For detailed output:
pytest tests/ -v

## Note
This tool generates synthetic data for development and testing purposes. It does not use real market data.