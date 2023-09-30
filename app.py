import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Reading the S&P csv file
df = pd.read_csv('https://raw.githubusercontent.com/rajinipreethajohn/SP500/main/SP500.csv', parse_dates=['Date'], index_col='Date')
df['Close'] = df['Close'].str.replace(',', '').astype(float)
df['Open'] = df['Open'].str.replace(',', '').astype(float)
df.rename(columns={'Return Close day vs Close previous day': 'Return'}, inplace=True)

# Calculate moving averages
df['ema_short'] = df['Close'].ewm(span=50, adjust=False).mean()
df['ema_long'] = df['Close'].ewm(span=200, adjust=False).mean()

# Streamlit app
st.title('S&P 500 Stock Analysis')

# Plotting the data using Plotly
st.write('## Close Price and Moving Averages for 50 and 200 days')
fig = go.Figure()

# Plotting Close price
fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price'))
# Plotting 50-day EMA
fig.add_trace(go.Scatter(x=df.index, y=df['ema_short'], mode='lines', name='50-day EMA', line=dict(color='orange')))
# Plotting 200-day EMA
fig.add_trace(go.Scatter(x=df.index, y=df['ema_long'], mode='lines', name='200-day EMA', line=dict(color='green')))

fig.update_layout(title='Close Price and Moving Averages', xaxis_title='Date', yaxis_title='Price')
st.plotly_chart(fig)

# Trading signals
df['Bullish'] = np.where(df['ema_short'] > df['ema_long'], 1.0, 0.0)
df['Crossover'] = df['Bullish'].diff()

st.write('## Trading Signals')
st.dataframe(df[['ema_short', 'ema_long', 'Bullish', 'Crossover']])

# Buy and Sell signals plot
st.write('## Buy and Sell Signals')
fig_signals = go.Figure()

# Plotting Close price
fig_signals.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price'))
# Plotting Buy signals
buy_signals = df[df['Crossover'] == 1.0]
fig_signals.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals['Close'], mode='markers', name='Buy Signal', marker=dict(color='green', size=10)))
# Plotting Sell signals
sell_signals = df[df['Crossover'] == -1.0]
fig_signals.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals['Close'], mode='markers', name='Sell Signal', marker=dict(color='red', size=10)))

fig_signals.update_layout(title='Buy and Sell Signals', xaxis_title='Date', yaxis_title='Price')
st.plotly_chart(fig_signals)
