import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('data/dpc-covid19-ita-regioni.csv')
df['data'] = pd.to_datetime(df['data'])

# Group by date (aggregate all regions)
df_daily = df.groupby('data', as_index=False)[['nuovi_positivi', 'dimessi_guariti']].sum()

# Create new columns
df_daily['New Recoveries'] = df_daily['dimessi_guariti'].diff()
df_daily = df_daily.rename(columns={
    'nuovi_positivi': 'New Cases',
})

fig = go.Figure()

# New cases
fig.add_trace(go.Scatter(
    x=df_daily['data'],
    y=df_daily['New Cases'],
    mode='lines',
    name='New Cases',
    hovertemplate='New Cases: %{y:.5s}<extra></extra>'
))

# New recoveries
fig.add_trace(go.Scatter(
    x=df_daily['data'],
    y=df_daily['New Recoveries'],
    mode='lines',
    name='New Recoveries',
    hovertemplate='New Recoveries: %{y:.5s}<extra></extra>'
))

# Customize layout
fig.update_layout(
    title='Newly Infected vs. Newly Recovered in Italy',
    xaxis_title='Date',
    yaxis_title='Number of People',
    legend_title='Group',
    hovermode='x unified'
)

fig.show()
fig.write_html('plots/inf_vs_rec.html')