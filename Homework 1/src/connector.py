#Connect to the Alpaca API
import os
from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient

load_dotenv()
ALPACA_API_KEY = os.getenv(ALPACA_API_KEY)
os.getenv(ALPACA_SECRET_KEY)

client = StockHistoricalDataClient(ALPACA_API_KEY = os.getenv(ALPACA_API_KEY)
, ALPACA_SECRET_KEY = os.getenv(ALPACA_SECRET_KEY))