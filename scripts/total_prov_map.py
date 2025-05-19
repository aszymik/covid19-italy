import requests
import plotly.express as px
import pandas as pd

italian_province_url = 'https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_provinces.geojson'
italy_geojson_province = requests.get(italian_province_url).json()

bbox = italy_geojson_province['bbox']
center = {"lat": 41.5, "lon": (bbox[2] + bbox[0]) / 2}


province_df =  pd.read_csv('data/dpc-covid19-ita-province.csv', na_values=[], keep_default_na=False)
cases_df = province_df[province_df['data'] == '2025-01-08T17:00:00']

fig = px.choropleth_mapbox(
    cases_df,
    geojson=italy_geojson_province,
    locations='sigla_provincia',
    featureidkey='properties.prov_acr',
    color='totale_casi',
    mapbox_style="carto-positron",
    zoom=5.3,
    center=center,
    labels={'totale_casi': 'Total Cases'},
    hover_name='denominazione_provincia',
    hover_data={'sigla_provincia': False, 'totale_casi': ':.4s'}

)
fig.update_geos(fitbounds="locations", visible=True)
fig.update_layout(
    title_text='Total COVID-19 Cases in Italy by Province',
    title_x=0.5,
    title_y=0.98,
    title_pad={"t": 40},
    margin={"r":0,"t":80,"l":0,"b":0},
    height=980,
    width=880
)

fig.write_html('plots/total_prov_map.html')