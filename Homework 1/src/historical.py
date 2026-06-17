from src.connector import get_historical_client
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def fetch_bars(ticker, days=30, timeframe=TimeFrame.Day):
    client = get_historical_client()
    param_request = StockBarsRequest(
        symbol_or_symbols=ticker,
        timeframe=timeframe,
        start=datetime.now() - timedelta(days=days)
    )
    bars = client.get_stock_bars(param_request)
    df = bars.df
    df = df.reset_index(level=0, drop=True)  # drop the symbol level, keep just timestamp
    return df


def get_day_data(df, selected_date):
    return df[df.index.date == selected_date]


def build_plot(df):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3], shared_xaxes=True)

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="OHLC"
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        x=df.index,
        y=df["volume"],
        name="Volume"
    ), row=2, col=1)

    show_slider = len(df) > 30
    fig.update_layout(xaxis_rangeslider_visible=show_slider)

    if len(df) <= 30:
        fig.update_xaxes(
            tickmode='array',
            tickvals=df.index,
            ticktext=[d.strftime('%b %d') for d in df.index]
        )

    return fig


if __name__ == "__main__":
    df = fetch_bars("AAPL")
    print(df)