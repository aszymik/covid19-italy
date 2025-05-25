import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('data/dpc-covid19-ita-regioni.csv')
df['data'] = pd.to_datetime(df['data'])

# Group by date (aggregate all regions)
df_daily = df.groupby('data', as_index=False)[['deceduti']].sum()

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_daily['data'],
    y=df_daily['deceduti'],
    mode='lines',
    name='Total Deaths',
    hovertemplate='Total Deaths: %{y:.5s}<extra></extra>'
))

# Customize layout
fig.update_layout(
    title='Total Coronavirus Deaths in Italy',
    xaxis_title='Date',
    yaxis_title='Total Deaths',
    legend_title='Legend',
    hovermode='x unified'
)

fig.write_html('plots/total_deaths.html')
