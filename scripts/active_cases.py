import pandas as pd
import plotly.express as px

df = pd.read_csv('data/dpc-covid19-ita-regioni.csv')
df['data'] = pd.to_datetime(df['data'])

# Group by date (aggregate all regions)
df_daily = df.groupby('data', as_index=False)[['totale_positivi']].sum()

# Plot active cases
fig = px.line(df_daily, x='data', y='totale_positivi',
                    labels={'data': 'Date', 'totale_positivi': 'Active Cases'})

fig.update_layout(
    title=dict(
        text='Active Cases in Italy',
        font=dict(size=24)
    ),
    xaxis=dict(
        title=dict(text='Date', font=dict(size=19)),
        tickfont=dict(size=15)
    ),
    yaxis=dict(
        title=dict(text='Active Cases', font=dict(size=19)),
        tickfont=dict(size=15)
    ),
    font=dict(size=13),
    hovermode='x unified'
)

fig.write_html('plots/active_cases.html')
fig.write_html('plots/active_cases.html')