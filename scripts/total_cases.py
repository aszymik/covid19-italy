import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('data/dpc-covid19-ita-regioni.csv')
df['data'] = pd.to_datetime(df['data'])

# Group by date (aggregate all regions)
df_daily = df.groupby('data', as_index=False)[['totale_casi']].sum()

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_daily['data'],
    y=df_daily['totale_casi'],
    mode='lines',
    name='Total Cases',
    hovertemplate='Total Infected: %{y:.5s}<extra></extra>'
))

# Customize layout
fig.update_layout(
    title='Total Coronavirus Cases in Italy',
    xaxis_title='Date',
    yaxis_title='Total Infected',
    legend_title='Legend',
    hovermode='x unified'
)

fig.write_html('plots/total_cases.html')