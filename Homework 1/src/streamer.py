import asyncio
import threading
from src.connector import get_stream_client

latest_quote = {"symbol": None, "bid": None, "ask": None, "last": None}
_lock = threading.Lock()

# Track the active stream so we can tear it down before starting a new one.
_active_stream = None
_active_stream = None
_active_thread = None
_active_symbol = None


def stop_stream():
    """Tear down any currently running stream before starting a new one."""
    global _active_stream, _active_thread, _active_symbol
    if _active_stream is not None:
        try:
            _active_stream.stop()  # safe to call from another thread
        except Exception as e:
            print(f"[streamer] error stopping stream: {e}")
    if _active_thread is not None:
        _active_thread.join(timeout=2) # wait for the old thread to die
    _active_stream = None
    _active_thread = None
    _active_symbol = None


def start_stream(symbol: str):
    global _active_stream, _active_thread, _active_symbol

    stop_stream()  # kill the previous symbol's connection first

    with _lock:
        latest_quote.update({"symbol": None, "bid": None, "ask": None, "last": None})

    _active_symbol = symbol

    # Quotes = the order book (resting bid/ask).
    async def quote_handler(quote):
        if quote.symbol != _active_symbol:   # ignore stragglers from old stream
            return
        with _lock:
            latest_quote["symbol"] = quote.symbol
            latest_quote["bid"] = quote.bid_price
            latest_quote["ask"] = quote.ask_price
            
 # Trades = actual executions, seperate from quotes
    async def trade_handler(trade):
        if trade.symbol != _active_symbol:
            return
        with _lock:
            latest_quote["symbol"] = trade.symbol
            latest_quote["last"] = trade.price

    stream = get_stream_client()

    def runner():
           # A background thread needs its own event loop
        asyncio.set_event_loop(asyncio.new_event_loop())
        stream.subscribe_quotes(quote_handler, symbol)
        stream.subscribe_trades(trade_handler, symbol)
        print(f"[streamer] connecting for {symbol}...")
        stream.run()        # blocks this thread forever

      # daemon=True -> dies with the app, no leaked socket.
    thread = threading.Thread(target=runner, daemon=True)
    _active_stream = stream
    _active_thread = thread
    thread.start()
    return thread


def get_latest():
    with _lock:
        return dict(latest_quote)
