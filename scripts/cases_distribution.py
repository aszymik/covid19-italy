import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("data/dpc-covid19-ita-regioni.csv", parse_dates=["data"])

italy_total = df.groupby("data").agg({
    "totale_positivi": "sum",
    "deceduti": "sum",
    "dimessi_guariti": "sum"
}).reset_index().rename(columns={
    "data": "date",
    "totale_positivi": "cumulative_positive_cases",
    "deceduti": "death",
    "dimessi_guariti": "recovered"
})

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=italy_total["date"],
    y=italy_total["cumulative_positive_cases"],
    name="Active",
    mode="none",
    fill="tonexty",
    fillcolor="#1f77b4",
    stackgroup="one"
))

fig.add_trace(go.Scatter(
    x=italy_total["date"],
    y=italy_total["death"],
    name="Death",
    mode="none",
    fill="tonexty",
    fillcolor="#E41317",
    stackgroup="one"
))

fig.add_trace(go.Scatter(
    x=italy_total["date"],
    y=italy_total["recovered"],
    name="Recovered",
    mode="none",
    fill="tonexty",
    fillcolor="forestgreen",
    stackgroup="one"
))

fig.update_layout(
    title="Italy - Distribution of Covid19 Cases",
    legend=dict(x=0.1, y=0.9),
    xaxis_title="Source: Italy Department of Civil Protection",
    yaxis_title="Number of Cases"
)

# fig.show()
fig.write_html('plots/cases_distribution.html')