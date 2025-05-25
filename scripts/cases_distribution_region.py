import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("data/dpc-covid19-ita-regioni.csv", parse_dates=["data"])

italy_region = df.rename(columns={
    "denominazione_regione": "region_name",
    "totale_positivi": "cumulative_positive_cases",
    "deceduti": "death",
    "dimessi_guariti": "recovered",
    "totale_casi": "cumulative_cases"
})

latest = italy_region[italy_region["data"] == italy_region["data"].max()].copy()
latest = latest[["region_name", "cumulative_positive_cases", "recovered", "death", "cumulative_cases"]]
latest = latest.sort_values("cumulative_cases", ascending=False)
latest["region"] = pd.Categorical(latest["region_name"], categories=latest["region_name"], ordered=True)

fig = go.Figure()

fig.add_trace(go.Bar(
    y=latest["region"],
    x=latest["cumulative_positive_cases"],
    name="Active",
    orientation="h",
    text=latest["cumulative_positive_cases"],
    textposition="auto",
    marker=dict(color="#1f77b4")
))

fig.add_trace(go.Bar(
    y=latest["region"],
    x=latest["recovered"],
    name="Recovered",
    orientation="h",
    text=latest["recovered"],
    textposition="auto",
    marker=dict(color="forestgreen")
))

fig.add_trace(go.Bar(
    y=latest["region"],
    x=latest["death"],
    name="Death",
    orientation="h",
    text=latest["death"],
    textposition="auto",
    marker=dict(color="red")
))

fig.update_layout(
    title="Cases Distribution by Region",
    barmode="stack",
    yaxis_title="Region",
    xaxis_title="Number of Cases",
    hovermode="x unified",
    legend=dict(x=0.65, y=0.9),
    margin=dict(l=20, r=10, b=10, t=30, pad=2)
)


# fig.show()
fig.write_html('plots/cases_distribution_region.html')