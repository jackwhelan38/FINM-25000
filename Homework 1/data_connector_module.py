# Data Connector Module
# - Loads API keys from environment variables
# - Connects to Alpaca’s Market Data API
# - Downloads historical data for a symbol you choose
# - Streams real‑time quotes (bid/ask)

from alpaca.data.historical import StockHistoricalDataClient

