from src.historical import fetch_bars

ticker = st.text_input("Ticker", value="AAPL").strip().upper()
df = fetch_bars(ticker)