import requests
import plotly.express as px
import pandas as pd

italian_province_url = 'https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_provinces.geojson'
italy_geojson_province = requests.get(italian_province_url).json()

bbox = italy_geojson_province['bbox']
center = {"lat": 41.5, "lon": (bbox[2] + bbox[0]) / 2}

province_df = pd.read_csv('data/dpc-covid19-ita-province.csv', na_values=[], keep_default_na=False)
pop_df = pd.read_csv('data/population_by_province.csv', keep_default_na=False, na_values=[])

cases_df = province_df[province_df['data'] == '2025-01-08T17:00:00']
cases_df = cases_df.merge(pop_df, on='sigla_provincia', how='left')
cases_df['cases_per_100k'] = (cases_df['totale_casi'] / cases_df['population']) * 100000

fig = px.choropleth_mapbox(
    cases_df,
    geojson=italy_geojson_province,
    locations='sigla_provincia',
    featureidkey='properties.prov_acr',
    color='cases_per_100k',
    mapbox_style="carto-positron",
    zoom=5.3,
    center=center,
    labels={
        'cases_per_100k': 'Total cases per 100k',
        'denominazione_provincia': 'Province'
    },
    hover_name='denominazione_provincia',
    hover_data={
        'sigla_provincia': False,
        'totale_casi': ':.4s',
        'cases_per_100k': ':.2f'
    }
)

fig.update_layout(
    title=dict(
        text='Confirmed COVID-19 Cases per 100k by Province (as of 2025-01-08)',
        font=dict(size=24),
        x=0.5,
        y=0.98,
        pad={"t": 40},
    ),
    font=dict(size=13),
    margin={"r": 0, "t": 80, "l": 0, "b": 0},
    height=980,
    width=880,
)

fig.write_html('plots/total_prov_map_100k.html')
