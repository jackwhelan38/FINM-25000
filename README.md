# FINM 25000 — Quantitative Portfolio Management & Algorithmic Trading

*Coursework, projects, and builds for FINM 25000.*


# Homework 1 — Mini Market Data Terminal

A Python application that authenticates to Alpaca's paper-trading API, retrieves
historical OHLCV data, and streams live bid/ask/last quotes, all displayed in a
Streamlit UI.

## Features

Authenticates to Alpaca via environment variables
Historical mode: 30 days of OHLCV bars as an interactive candlestick + volume
chart, with a day-selector to drill into 5-minute intraday detail
Live mode: real-time Bid / Ask / Last over a WebSocket, auto-updating

## Architecture

**`connector.py`** — Loads Alpaca API keys from environment variables and exposes two factory functions: `get_historical_client()`
for REST data and `get_stream_client()` for the live WebSocket feed (pinned to the
IEX feed).

**`historical.py`** — Fetches historical OHLCV bars via `fetch_bars()`, filters to a
single day with `get_day_data()` for the intraday drill-down, and renders an
interactive Plotly candlestick + volume chart with `build_plot()`.

**`streamer.py`** — Runs the async quote and trade streamsnon a background daemon thread, writing the latest Bid/Ask/Last into a lock-guarded
shared buffer that the UI reads via `get_latest()`. Manages stream lifecycle
(`start_stream()` / `stop_stream()`) so switching tickers cleanly tears down the old
connection before opening a new one.

**`app.py`** — The Streamlit UI. A sidebar toggle switches between Historical mode
(candlestick charts with a day-selector) and Live mode (real-time Bid/Ask/Last that
auto-refreshes every second).

## Setup

### 1. Navigate to Appropriate Folder
cd "Homework 1"

### 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate          

### 3. Install dependencies
pip install -r requirements.txt

### 4. Add your Alpaca paper keys to a .env file in this folder:
    ALPACA_API_KEY=your_key_id
    ALPACA_SECRET_KEY=your_secret_key

### 5. Run
streamlit run app.py

## Demo

📹 Video walkthrough: [LINK TO DEMO VIDEO]

## Notes & Limitations

Live quotes stream from Alpaca's free IEX feed (a single exchange), so
bid/ask reflect IEX's book rather than the consolidated NBBO seen on retail
sites — prices may differ slightly.
Quotes only stream during market hours (9:30 AM–4:00 PM ET, Mon–Fri).
Free tier allows one live WebSocket connection at a time.


## Contributors

*Jack Whelan* — historical data + charting (historical.py), Historical UI

*Harry Murphy* — live streaming layer (streamer.py), Live UI branch

