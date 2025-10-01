# OHLC Data Aggregation and Analysis Tool

A Python tool for generating synthetic OHLC price data and aggregating it to multiple timeframes with financial metrics and visualization.

## Features

- Generate realistic 1-minute OHLC data for trading days
- Aggregate to 5-minute, 30-minute, and 1-day timeframes
- Calculate metrics (VWAP, moving average, moving median)
- Visualization with timeframe switching
- Test coverage

## Requirements

- pandas
- numpy
- plotly
- pytest

## Quick Start

```bash
git clone <repository-url>
```

```bash
cd ohlc-processor
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the complete example

```bash
python main.py
```

## Testing

```bash
pytest tests/
```
#### For detailed output:

```bash
pytest tests/ -v
```

## Note
This tool generates synthetic data for development and testing purposes. It does not use real market data.