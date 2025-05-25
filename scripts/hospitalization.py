import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("data/dpc-covid19-ita-regioni.csv", parse_dates=["data"])

italy_total = df.groupby("data").agg({
    "isolamento_domiciliare": "sum",
    "ricoverati_con_sintomi": "sum",
    "terapia_intensiva": "sum"
}).reset_index()

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=italy_total["data"],
    y=italy_total["isolamento_domiciliare"],
    name='Home Confinement',
    mode='none',
    fill='tonexty',
    fillcolor='#FDBBBC',
    stackgroup='one'
))

fig.add_trace(go.Scatter(
    x=italy_total["data"],
    y=italy_total["ricoverati_con_sintomi"],
    name='Hospitalized with Symptoms',
    mode='none',
    fill='tonexty',
    fillcolor='#E41317',
    stackgroup='one'
))

fig.add_trace(go.Scatter(
    x=italy_total["data"],
    y=italy_total["terapia_intensiva"],
    name='Intensive Care',
    mode='none',
    fill='tonexty',
    fillcolor='#9E0003',
    stackgroup='one'
))

fig.update_layout(
    title=dict(
        text='Italy - Distribution of Active Covid19 Cases',
        font=dict(size=24)
    ),
    # xaxis=dict(
    #     title=dict(text='Source: Italy Department of Civil Protection', font=dict(size=19)),
    #     tickfont=dict(size=15)
    # ),
    yaxis=dict(
        title=dict(text='Number of Cases', font=dict(size=19)),
        tickfont=dict(size=15)
    ),
    legend=dict(
        title=dict(text='Legend', font=dict(size=17)),
        font=dict(size=15),
        x=0.8, 
        y=0.9
    ),
    font=dict(size=13),
    hovermode='x unified'
)

# fig.show()
fig.write_html('plots/hospitalization.html')
# fig.show()
fig.write_html('plots/hospitalization.html')