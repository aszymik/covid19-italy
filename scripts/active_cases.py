import pandas as pd
import plotly.express as px

df = pd.read_csv('data/dpc-covid19-ita-regioni.csv')
df['data'] = pd.to_datetime(df['data'])

# Group by date (aggregate all regions)
df_daily = df.groupby('data', as_index=False)[['totale_positivi']].sum()

# Plot active cases
fig = px.line(df_daily, x='data', y='totale_positivi',
                    title='Active Cases in Italy',
                    labels={'data': 'Date', 'totale_positivi': 'Active Cases'})

fig.write_html('plots/active_cases.html')