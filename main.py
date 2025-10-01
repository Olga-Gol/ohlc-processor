from src.data_generator import generate_1min_ohlc
from src.aggregator import aggregate_to_5min, aggregate_to_30min, aggregate_to_1d
from src.metrics import add_metrics_to_5min, add_metrics_to_30min 
from src.visualization import create_interactive_chart

def main():
    df_1min = generate_1min_ohlc(start_price=100.0, seed=42)
    df_5min = aggregate_to_5min(df_1min)
    df_30min = aggregate_to_30min(df_1min) 
    df_1d = aggregate_to_1d(df_1min)

    # Add metrics to aggregated data
    df_5min_with_metrics = add_metrics_to_5min(df_5min)
    df_30min_with_metrics = add_metrics_to_30min(df_30min)

    print(f"Generated {len(df_1min)} 1-minute bars")

    print(f"Time range: {df_1min.index[0]} to {df_1min.index[-1]}")
    print("\n1-minute data (first 10 bars):")
    print(df_1min.head(10))

    print("\n5-minute data (first 5 bars) with metrics:")
    print(df_5min_with_metrics.head())

    print("\n30-minute data (first 5 bars) with metrics:")
    print(df_30min_with_metrics.head())

    print("\n1-day data:")
    print(df_1d.head())

    fig = create_interactive_chart(df_1min, df_5min_with_metrics, df_30min_with_metrics, df_1d)
    fig.show()

if __name__ == "__main__":
    main()