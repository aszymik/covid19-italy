import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('data/dpc-covid19-ita-regioni.csv')
df['data'] = pd.to_datetime(df['data'])

# Drop rows with missing province names (often summary rows)
df = df.dropna(subset=['denominazione_regione'])

# Rename columns for clarity
df = df.rename(columns={
    'denominazione_regione': 'Province',
    'nuovi_positivi': 'New Cases',
    'data': 'Date'
})

# Group by month and province
df['Month'] = df['Date'].dt.to_period('M').dt.to_timestamp()
df_monthly = df.groupby(['Month', 'Province'], as_index=False)['New Cases'].max()

# Filter provinces with high case counts (optional for clarity)
province_totals = df_monthly.groupby('Province')['New Cases'].max()
top_provinces = province_totals[province_totals > 5000].index
df_monthly = df_monthly[df_monthly['Province'].isin(top_provinces)]

# Sort for better frame order
df_monthly = df_monthly.sort_values(['Month', 'New Cases'], ascending=[True, False])

# Create animated bar plot
fig = px.bar(
    df_monthly,
    x='New Cases',
    y='Province',
    color='Province',
    animation_frame=df_monthly['Month'].dt.strftime('%Y-%m'),  # Monthly animation frame
    animation_group='Province',
    orientation='h',
    range_x=[0, df_monthly['New Cases'].max() * 1.05],
    title='Monthly Active COVID-19 Cases per Province in Italy',
    labels={'New Cases': 'Total New Cases', 'Province': 'Province'},
    height=700
)

# Layout customization
fig.update_layout(
    xaxis_title='Total New Cases in a Month',
    yaxis_title='Province',
    showlegend=False,
    hovermode='x unified',
    transition={'duration': 300}
)

fig.show()
fig.write_html('plots/animated_province_cases_by_month.html')
