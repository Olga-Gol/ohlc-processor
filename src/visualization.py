import plotly.graph_objects as go

def create_interactive_chart(df_1min, df_5min_with_metrics, df_30min_with_metrics, df_1d):
    fig = go.Figure()
    
    # Add all OHLC data (initially only 1-min visible)
    # 1-min OHLC
    fig.add_trace(go.Ohlc(
        x=df_1min.index,
        open=df_1min['Open'],
        high=df_1min['High'],
        low=df_1min['Low'],
        close=df_1min['Close'],
        name='OHLC'
    ))
    
    # 5-min OHLC 
    fig.add_trace(go.Ohlc(
        x=df_5min_with_metrics.index,
        open=df_5min_with_metrics['Open'],
        high=df_5min_with_metrics['High'],
        low=df_5min_with_metrics['Low'],
        close=df_5min_with_metrics['Close'], 
        name='OHLC',
        visible=False
    ))
    
    # 5-min MA 
    fig.add_trace(go.Scatter(
        x=df_5min_with_metrics.index,
        y=df_5min_with_metrics['MA_30min'],
        name='30-min MA',
        line=dict(color='blue'),
        visible=False
    ))
    
    # 5-min Median 
    fig.add_trace(go.Scatter(
        x=df_5min_with_metrics.index,
        y=df_5min_with_metrics['Median_15min'],
        name='15-min Median',
        line=dict(color='purple'),
        visible=False
    ))
    
    # 5-min VWAP
    fig.add_trace(go.Scatter(
        x=df_5min_with_metrics.index,
        y=df_5min_with_metrics['VWAP'],
        name='VWAP',
        line=dict(color='red'),
        visible=False
    ))
    
    # 30-min OHLC 
    fig.add_trace(go.Ohlc(
        x=df_30min_with_metrics.index,
        open=df_30min_with_metrics['Open'],
        high=df_30min_with_metrics['High'],
        low=df_30min_with_metrics['Low'],
        close=df_30min_with_metrics['Close'],
        name='OHLC',
        visible=False
    ))
    
    # 30-min VWAP 
    fig.add_trace(go.Scatter(
        x=df_30min_with_metrics.index,
        y=df_30min_with_metrics['VWAP'],
        name='VWAP',
        line=dict(color='red'),
        visible=False
    ))
    
    # 1-day OHLC 
    fig.add_trace(go.Ohlc(
        x=df_1d.index,
        open=df_1d['Open'],
        high=df_1d['High'],
        low=df_1d['Low'],
        close=df_1d['Close'],
        name='OHLC',
        visible=False
    ))
    
    # Timeframe buttons 
    timeframe_buttons = [
        dict(
            label="1-MINUTE",
            method="update",
            args=[{"visible": [True] + [False]*7}, 
                  {"title": "1-Minute OHLC Data"}]
        ),
        dict(
            label="5-MINUTE", 
            method="update",
            args=[{"visible": [False, True, True, True, True] + [False]*3},  
                  {"title": "5-Minute OHLC with Metrics"}]
        ),
        dict(
            label="30-MINUTE",
            method="update", 
            args=[{"visible": [False]*5 + [True, True] + [False]},  
                  {"title": "30-Minute OHLC with VWAP"}]
        ),
        dict(
            label="1-DAY",
            method="update",
            args=[{"visible": [False]*7 + [True]},  
                  {"title": "1 day OHLC Data"}]
        )
    ]
    
    fig.update_layout(
        title={
            'text': '1-Minute OHLC Data',  
            'x': 0.03,
            'xanchor': 'left',
            'yanchor': 'top',
        },
        margin=dict(t=80, b=50, l=50, r=50), 
        updatemenus=[dict(
            buttons=timeframe_buttons,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.5,   
            xanchor="center",
            y=1.15,   
            yanchor="top"
        )]
    )
    
    return fig