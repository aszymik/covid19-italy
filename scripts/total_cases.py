import pandas as pd
import plotly.express as px

df = pd.read_csv('data/dpc-covid19-ita-regioni.csv')
df['data'] = pd.to_datetime(df['data'])

# Group by date (aggregate all regions)
df_daily = df.groupby('data', as_index=False)[['totale_casi']].sum()

# Plot total cases
fig = px.line(df_daily, x='data', y='totale_casi',
              title='Total Coronavirus Cases in Italy',
              labels={'data': 'Date', 'totale_casi': 'Total Coronavirus Currently Infected'})

fig.write_html('plots/total_cases.html')