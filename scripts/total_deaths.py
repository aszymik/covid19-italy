import pandas as pd
import plotly.express as px

df = pd.read_csv('data/dpc-covid19-ita-regioni.csv')
df['data'] = pd.to_datetime(df['data'])

# Group by date (aggregate all regions)
df_daily = df.groupby('data', as_index=False)[['deceduti']].sum()

# Plot total deaths
fig = px.line(df_daily, x='data', y='deceduti',
                     title='Total Coronavirus Deaths in Italy',
                     labels={'data': 'Date', 'deceduti': 'Total Deaths'})
fig.show()
