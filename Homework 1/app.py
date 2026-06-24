import streamlit as st
from datetime import datetime
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from src.historical import build_plot, fetch_bars, get_day_data
from src.streamer import start_stream, get_latest
import time

st.title('Homework #1: Mini Market Data Terminal')

ticker = st.text_input("Ticker", value="AAPL").strip().upper()
data_type = st.sidebar.selectbox("Data Type", ['Historical', 'Live'])

# Placeholder we fully control — guarantees the intraday chart is
# physically removed from the page, instead of relying on Streamlit's
# diffing to figure out it should disappear.
intraday_slot = st.empty()

if data_type == 'Historical':

    if st.button('Load Chart'):

        if not ticker.isalpha() or len(ticker) > 5:
            st.write("Please enter a valid ticker symbol (letters only, up to 5 characters).")
            st.stop()

        try:
            daily_summary = fetch_bars(ticker, days=30, timeframe=TimeFrame.Day)
        except Exception as e:
            st.write(f"Couldn't find data for '{ticker}'. Check the ticker symbol and try again.")
            st.stop()

        summary_fig = build_plot(daily_summary)
        st.plotly_chart(summary_fig, use_container_width=True)

        st.session_state['available_days'] = list(daily_summary.index.date)
        st.session_state['ticker'] = ticker

    if 'available_days' in st.session_state:
        with intraday_slot.container():
            selected_day = st.selectbox(
                'Select Day for intraday detail',
                options=st.session_state['available_days']
            )

            all_bars = fetch_bars(st.session_state['ticker'], days=30, timeframe=TimeFrame(5, TimeFrameUnit.Minute))
            single_day = get_day_data(all_bars, selected_day)

            if single_day.empty:
                st.write('Daily data unavailable')
            else:
                st.subheader(f'Intraday detail: {selected_day}')
                intra_day_fig = build_plot(single_day)
                st.plotly_chart(intra_day_fig, use_container_width=True)
    else:
        intraday_slot.empty()

elif data_type == 'Live':
    intraday_slot.empty()   # force-clear it, don't trust reconciliation alone

    for key in ['available_days', 'ticker']:
        st.session_state.pop(key, None)
    st.subheader(f'Live Quotes: {ticker}')

    if st.session_state.get('streaming_ticker') != ticker:
        start_stream(ticker)
        st.session_state['streaming_ticker'] = ticker

    quote = get_latest()

    col1, col2, col3 = st.columns(3)
    col1.metric("Bid", quote['bid'] if quote['bid'] is not None else "—")
    col2.metric("Ask", quote['ask'] if quote['ask'] is not None else "—")
    col3.metric("Last", quote['last'] if quote['last'] is not None else "—")

    if quote['bid'] is None:
        st.caption("Waiting for quotes… (market may be closed — opens 9:30am–4pm ET, Mon–Fri)")

    time.sleep(1)
    st.rerun()