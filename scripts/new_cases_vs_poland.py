import pandas as pd
import plotly.graph_objects as go

# Dates intersection
start_date = '2020-02-24'
end_date = '2024-08-04'

pop_italy = 60_000_000
pop_poland = 38_000_000

# Italy data
df_it = pd.read_csv('data/dpc-covid19-ita-regioni.csv')
df_it['data'] = pd.to_datetime(df_it['data'])

# Sum new cases in weeks
df_it['Week'] = df_it['data'].dt.to_period('W').dt.to_timestamp()
df_weekly = df_it.groupby(['Week'], as_index=False)['nuovi_positivi'].sum()
df_weekly.set_index('Week', inplace=True)
df_weekly = df_weekly[:end_date]

# Normalize per 100k
df_weekly['norm_cases_italy'] = df_weekly['nuovi_positivi'] / pop_italy * 100_000

# Poland data
df_pl = pd.read_csv('data/weekly_cases.csv')
df_pl = df_pl[['date', 'Poland']]
df_pl['date'] = pd.to_datetime(df_pl['date'])
df_pl.set_index('date', inplace=True)
df_pl = df_pl[start_date:end_date]

# Normalize per 100k
df_pl['norm_cases_poland'] = df_pl['Poland'] / pop_poland * 100_000

fig = go.Figure()

# Italy
fig.add_trace(go.Scatter(
    x=df_weekly.index,
    y=df_weekly['norm_cases_italy'],
    mode='lines',
    name='Weekly New Cases in Italy (per 100k)',
    hovertemplate='Italy: %{y:.2f} / 100k<extra></extra>'
))

# Poland
fig.add_trace(go.Scatter(
    x=df_pl.index,
    y=df_pl['norm_cases_poland'],
    mode='lines',
    name='Weekly New Cases in Poland (per 100k)',
    hovertemplate='Poland: %{y:.2f} / 100k<extra></extra>'
))

fig.update_layout(
    title=dict(
        text='Weekly New COVID-19 Cases per 100,000 Citizens: Italy vs. Poland',
        font=dict(size=24)
    ),
    xaxis=dict(
        title=dict(text='Date', font=dict(size=19)),
        tickfont=dict(size=15)
    ),
    yaxis=dict(
        title=dict(text='New Cases per 100k', font=dict(size=19)),
        tickfont=dict(size=15)
    ),
    legend=dict(
        title=dict(text='Legend', font=dict(size=17)),
        font=dict(size=15)
    ),
    font=dict(size=13),
    hovermode='x unified'
)

fig.write_html('plots/new_cases_vs_poland.html')