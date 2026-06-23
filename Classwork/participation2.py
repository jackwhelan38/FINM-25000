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

# 3
signals = pd.DataFrame(index=goog_data.index)

# 4
signals['signal'] = [random.randint(0,1) for i in range(len(signals))]
signals['close'] = goog_data['Close']

# 5
signals['orders'] = signals['signal'].diff()

# 6
buys = signals[signals['orders'] == 1]
sells = signals[signals['orders'] == -1]

plt.figure(figsize=(14, 6))
plt.plot(signals.index, signals['close'], label='GOOG Close Price', color='blue', alpha=0.7)
plt.scatter(buys.index,  buys['close'],  marker='^', color='green', label='Buy (+1)',  s=100)
plt.scatter(sells.index, sells['close'], marker='v', color='red',   label='Sell (-1)', s=100)
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.tight_layout()
plt.show()

# 7
initial_capital = 10000
shares = 100

portfolio = pd.DataFrame(index=signals.index)

# 8
portfolio['holding'] = signals['signal'] * shares * signals['close']
portfolio['cash'] = initial_capital - (signals['orders'] * shares * signals['close']).cumsum()
portfolio['total'] = portfolio['cash'] + portfolio['holding']

# 9
plt.figure(figsize=(14, 6))
plt.plot(portfolio.index, portfolio['total'],   label='Total Value', color='blue')
plt.plot(portfolio.index, portfolio['cash'],    label='Cash',        color='green')
plt.plot(portfolio.index, portfolio['holding'], label='Holding',     color='orange')
plt.title('Portfolio Performance Over Time')
plt.xlabel('Date')
plt.ylabel('Value (USD)')
plt.legend()
plt.tight_layout()
plt.show()