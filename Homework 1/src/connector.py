# Connect to the Alpaca API
import os
from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.live import StockDataStream
from alpaca.data.enums import DataFeed

def get_historical_client():
    load_dotenv()
    API_KEY = os.getenv('ALPACA_API_KEY')
    SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
    client = StockHistoricalDataClient(API_KEY, SECRET_KEY)
    return client

def get_stream_client():                               # <-- ADD (after his function)
    load_dotenv()
    API_KEY = os.getenv('ALPACA_API_KEY')
    SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
    return StockDataStream(API_KEY, SECRET_KEY, feed=DataFeed.IEX)

if __name__ == '__main__':
    client = get_historical_client()
    print(client)
