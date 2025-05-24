import pandas as pd
import plotly.graph_objects as go

# Dates intersection
start_date = '2020-02-24'
end_date = '2024-08-04'

# Italy data
df_it = pd.read_csv('data/dpc-covid19-ita-regioni.csv')
df_it['data'] = pd.to_datetime(df_it['data'])

# Sum new cases in weeks
df_it['Week'] = df_it['data'].dt.to_period('W').dt.to_timestamp()
df_weekly = df_it.groupby(['Week'], as_index=False)['nuovi_positivi'].sum()
df_weekly.set_index('Week', inplace=True)
df_weekly = df_weekly[:end_date]

# Poland data
df_pl = pd.read_csv('data/weekly_cases.csv')
df_pl = df_pl[['date', 'Poland']]
df_pl.set_index('date', inplace=True)
df_pl = df_pl[start_date:end_date]



fig = go.Figure()

# Weekly new cases in Italy
fig.add_trace(go.Scatter(
    x=df_weekly.index,
    y=df_weekly['nuovi_positivi'],
    mode='lines',
    name='Weekly New Cases in Italy',
    hovertemplate='New Cases in Italy: %{y:.4s}<extra></extra>'
))

# Weekly new cases in Poland
fig.add_trace(go.Scatter(
    x=df_pl.index,
    y=df_pl['Poland'],
    mode='lines',
    name='Weekly New Cases in Poland',
    hovertemplate='New Cases in Poland: %{y:.4s}<extra></extra>'
))


# Customize layout
fig.update_layout(
    title='Weekly New COVID-19 Cases in Italy vs. Poland',
    xaxis_title='Date',
    yaxis_title='New Cases',
    legend_title='Legend',
    hovermode='x unified',
)

fig.show()
fig.write_html('plots/new_cases_vs_poland.html')