import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('data/dpc-covid19-ita-regioni.csv')
df['data'] = pd.to_datetime(df['data'])

# Group by date (aggregate all regions)
df_daily = df.groupby('data', as_index=False)[['deceduti']].sum()
df_daily['nuovi_deceduti'] = df_daily['deceduti'].diff()

# Compute 7-day moving average
df_daily['ma_7'] = df_daily['nuovi_deceduti'].rolling(window=7, center=True).mean()

fig = go.Figure()

# Daily deaths
fig.add_trace(go.Scatter(
    x=df_daily['data'],
    y=df_daily['nuovi_deceduti'],
    mode='lines',
    name='Daily Deaths',
    hovertemplate='New Deaths: %{y:.0f}<extra></extra>'
))

# 7-day moving average
fig.add_trace(go.Scatter(
    x=df_daily['data'],
    y=df_daily['ma_7'],
    mode='lines',
    name='7-Day Moving Average',
    line=dict(color='orange'),
    hovertemplate='7-Day Average: %{y:.4s}<extra></extra>'
))

# Customize layout
fig.update_layout(
    title='Daily Coronavirus Deaths in Italy',
    xaxis_title='Date',
    yaxis_title='Number of Deaths',
    legend_title='Legend',
    hovermode='x unified',
)

fig.write_html('plots/daily_deaths.html')