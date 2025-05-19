import pandas as pd
import plotly.express as px

df = pd.read_csv('data/dpc-covid19-ita-regioni.csv')
df['data'] = pd.to_datetime(df['data'])

# Group by date (aggregate all regions)
df_daily = df.groupby('data', as_index=False)[['nuovi_positivi', 'dimessi_guariti']].sum()

# Create new columns
df_daily['New Recoveries'] = df_daily['dimessi_guariti'].diff()
df_daily = df_daily.rename(columns={
    'nuovi_positivi': 'New Cases',
})

fig = px.line(
    df_daily, x='data', y=['New Cases', 'New Recoveries'],
    title='Newly Infected vs. Newly Recovered in Italy',
    labels={'value': 'New Daily Coronavirus Cases + Cured', 'variable': 'Group', 'data': 'Date'}
)
fig.show()