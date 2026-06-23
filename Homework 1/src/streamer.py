import asyncio
import threading

from src.connector import get_stream_client


# --- SHARED STATE: written by the stream thread, read by the UI ---
# A dict guarded by a Lock. Single writer (stream), single reader (UI).
latest_quote = {"symbol": None, "bid": None, "ask": None, "last": None}
_lock = threading.Lock()



# CONSOLE VERSION (standalone test — keep it)

def stream_quotes(symbol: str, on_quote=None):
    stream = get_stream_client()

    async def default_handler(quote):
        print(f"{quote.symbol}  bid={quote.bid_price}  ask={quote.ask_price}  @ {quote.timestamp}")

    handler = on_quote if on_quote is not None else default_handler
    stream.subscribe_quotes(handler, symbol)
    stream.run()


# THREADED VERSION (what the UI calls)

def start_stream(symbol: str):
    with _lock:
        latest_quote.update({"symbol": None, "bid": None, "ask": None, "last": None})

    async def quote_handler(quote):
        with _lock:
            latest_quote["symbol"] = quote.symbol
            latest_quote["bid"] = quote.bid_price
            latest_quote["ask"] = quote.ask_price

    async def trade_handler(trade):
        with _lock:
            latest_quote["symbol"] = trade.symbol
            latest_quote["last"] = trade.price

    def runner():
        asyncio.set_event_loop(asyncio.new_event_loop())
        stream = get_stream_client()
        stream.subscribe_quotes(quote_handler, symbol)
        stream.subscribe_trades(trade_handler, symbol)
        print(f"[streamer] connecting for {symbol}...")
        stream.run()

    thread = threading.Thread(target=runner, daemon=True)
    thread.start()
    return thread


def get_latest():
    with _lock:
        return dict(latest_quote)   # return a copy so the UI never holds the lock


if __name__ == "__main__":
    stream_quotes("AAPL")