import pandas as pd
import plotly.express as px

df = pd.read_csv('data/dpc-covid19-ita-regioni.csv')
df['data'] = pd.to_datetime(df['data'])

df = df.dropna(subset=['denominazione_regione'])  # drop rows with missing province names
df = df.rename(columns={
    'denominazione_regione': 'Region',
    'nuovi_positivi': 'New Cases',
    'data': 'Date'
})

# Group by month and province
df['Month'] = df['Date'].dt.to_period('M').dt.to_timestamp()
df_monthly = df.groupby(['Month', 'Region'], as_index=False)['New Cases'].max()

# Filter provinces with high case counts
province_totals = df_monthly.groupby('Region')['New Cases'].max()
top_provinces = province_totals[province_totals > 5000].index
df_monthly = df_monthly[df_monthly['Region'].isin(top_provinces)]

# Sort for better frame order
df_monthly = df_monthly.sort_values(['Month', 'New Cases'], ascending=[True, False])

fig = px.bar(
    df_monthly,
    x='New Cases',
    y='Region',
    color='Region',
    animation_frame=df_monthly['Month'].dt.strftime('%Y-%m'),  # Monthly animation frame
    animation_group='Region',
    orientation='h',
    range_x=[0, df_monthly['New Cases'].max() * 1.05],
    title='Monthly Active COVID-19 Cases per Region in Italy',
    labels={'New Cases': 'Total New Cases', 'Region': 'Region'},
    height=700
)

fig.update_layout(
    title=dict(
        text='Monthly Active COVID-19 Cases per Region in Italy',
        font=dict(size=24)
    ),
    xaxis=dict(
        title=dict(text='Total New Cases in a Month', font=dict(size=19)),
        tickfont=dict(size=15)
    ),
    yaxis=dict(
        title=dict(text='Region', font=dict(size=19)),
        tickfont=dict(size=15)
    ),
    showlegend=False,
    font=dict(size=13),
    hovermode='x unified',
    transition={'duration': 300}
)

fig.show()
fig.write_html('plots/animated_region_cases_by_month.html')
