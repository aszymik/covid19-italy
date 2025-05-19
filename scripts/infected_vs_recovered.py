import pandas as pd
import plotly.express as px

df = pd.read_csv('data/dpc-covid19-ita-regioni.csv')
df['data'] = pd.to_datetime(df['data'])

# Group by date (aggregate all regions)
df_daily = df.groupby('data', as_index=False)[['nuovi_positivi', 'dimessi_guariti']].sum()
df_daily['nuovi_guariti'] = df_daily['dimessi_guariti'].diff()

fig = px.line(
    df_daily, x='data', y=['nuovi_positivi', 'nuovi_guariti'],
    title='Newly Infected vs. Newly Recovered in Italy',
    labels={'value': 'New Daily Coronavirus Cases + Cured', 'variable': 'Category', 'data': 'Date'}
)
fig.show()