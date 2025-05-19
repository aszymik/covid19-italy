import pandas as pd
import plotly.express as px

df = pd.read_csv('data/dpc-covid19-ita-regioni.csv')
df['data'] = pd.to_datetime(df['data'])

# Group by date (aggregate all regions)
df_daily = df.groupby('data', as_index=False)[['nuovi_positivi']].sum()

# Plot new cases
fig = px.line(df_daily, x='data', y='nuovi_positivi',
                    title='Daily New Cases in Italy',
                    labels={'data': 'Date', 'nuovi_positivi': 'New Cases'})
fig.show()