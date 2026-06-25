# Connect to the Alpaca API
import os
from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.live import StockDataStream
from alpaca.data.enums import DataFeed

# REST client for historical OHLCV bars (request/response)
def get_historical_client():
    load_dotenv()
    API_KEY = os.getenv('ALPACA_API_KEY')
    SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
    client = StockHistoricalDataClient(API_KEY, SECRET_KEY)
    return client

# WebSocket client for live quotes/trades 
def get_stream_client():                             
    load_dotenv()
    API_KEY = os.getenv('ALPACA_API_KEY')
    SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
    return StockDataStream(API_KEY, SECRET_KEY, feed=DataFeed.IEX)

# Test to confirm auth function
if __name__ == '__main__':
    client = get_historical_client()
    print(client)
