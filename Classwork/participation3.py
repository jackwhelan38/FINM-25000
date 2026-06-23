import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import random

plt.style.use('default')

start_date = '2001-01-01'
end_date = '2018-01-01'
random.seed(6666)

# 1
goog_data = yf.download(
    'GOOG',
    start=start_date,
    end=end_date,
    auto_adjust=True
)
goog_data.head()

# 2
signals = pd.DataFrame(index=goog_data.index)

signals['short_ma'] = goog_data['Close'].rolling(window=40).mean()
signals['long_ma'] = goog_data['Close'].rolling(window=100).mean()

# 3
signals['signal'] = np.select(
    [
        signals['short_ma'] > signals['long_ma'],
        signals['short_ma'] < signals['long_ma'],
    ],
    [1.0, -1.0],
    default=0.0
)

signals['orders'] = signals['signal'].diff()

# 4
fig, ax = plt.subplots(figsize=(14, 7))

ax.plot(goog_data.index, goog_data['Close'], label='Close Price', alpha=0.5, color='gray')
ax.plot(signals.index, signals['short_ma'], label='40-day MA', color='blue')
ax.plot(signals.index, signals['long_ma'], label='100-day MA', color='orange')

ax.scatter(
    signals[signals['orders'] > 0].index,
    goog_data.loc[signals['orders'] > 0, 'Close'],
    marker='^', color='green', label='Long Signal', zorder=5, s=100
)

ax.scatter(
    signals[signals['orders'] < 0].index,
    goog_data.loc[signals['orders'] < 0, 'Close'],
    marker='v', color='red', label='Short Signal', zorder=5, s=100
)

ax.set_title("Google (GOOG) MA Crossover Strategy")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.legend()
plt.tight_layout()
plt.show()

# 5,6
initial_capital = 10000
shares = 100

portfolio = pd.DataFrame(index=signals.index)

signals['close'] = goog_data['Close']  # add close price to signals for convenience

portfolio['position'] = signals['signal'] * shares
portfolio['holdings'] = signals['signal'] * shares * signals['close']
portfolio['cash'] = initial_capital - (signals['orders'] * shares * signals['close']).cumsum()
portfolio['total'] = portfolio['cash'] + portfolio['holdings']

# 7
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 7), sharex=True)

ax1.plot(portfolio.index, portfolio['total'], color='blue', label='Total Portfolio Value')
ax1.set_ylabel("Value ($)")
ax1.legend()

ax2.plot(portfolio.index, portfolio['cash'], color='green', label='Cash')
ax2.set_ylabel("Value ($)")
ax2.legend()

ax3.plot(portfolio.index, portfolio['holdings'], color='orange', label='Holdings Value')
ax3.set_ylabel("Value ($)")
ax3.set_xlabel("Date")
ax3.legend()

fig.suptitle("Portfolio Performance Over Time")
plt.tight_layout()
plt.show()