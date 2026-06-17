# Gather Historical Data
from src.connector import get_historical_client
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta

def fetch_bars(ticker, days=30):
    client = get_historical_client()
    param_request = StockBarsRequest(
        symbol_or_symbols=ticker,
        timeframe=TimeFrame.Minute,
        start=datetime.now() - timedelta(days=days)
    )
    bars = client.get_stock_bars(param_request)
    return bars.df

if __name__ == '__main__':
    df = fetch_bars('AAPL')
    print(df)
