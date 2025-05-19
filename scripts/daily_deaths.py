import pandas as pd
import plotly.express as px

df = pd.read_csv('data/dpc-covid19-ita-regioni.csv')
df['data'] = pd.to_datetime(df['data'])

# Group by date (aggregate all regions)
df_daily = df.groupby('data', as_index=False)[['deceduti']].sum()
df_daily['nuovi_deceduti'] = df_daily['deceduti'].diff()

fig = px.line(df_daily, x='data', y='nuovi_deceduti',
                         title='Daily New Deaths in Italy',
                         labels={'data': 'Date', 'nuovi_deceduti': 'New Deaths'})
fig.show()