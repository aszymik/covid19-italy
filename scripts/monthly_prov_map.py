import pandas as pd
import requests
import plotly.express as px
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 0)
pd.set_option('display.max_colwidth', None)

italian_province_url = 'https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_provinces.geojson'
italy_geojson_province = requests.get(italian_province_url).json()

bbox = italy_geojson_province['bbox']
center = {"lat": 41.5, "lon": (bbox[2] + bbox[0]) / 2}

province_df = pd.read_csv('data/dpc-covid19-ita-province.csv', na_values=[], keep_default_na=False)
province_df = province_df[province_df['sigla_provincia'].str.len() == 2]
province_df = province_df[['data', 'denominazione_provincia', 'sigla_provincia', 'totale_casi']]
province_df['data'] = pd.to_datetime(province_df['data'])

def smooth_anomalies(df):
    df = df.sort_values('data').copy()
    x = df['totale_casi'].values
    med = pd.Series(x).rolling(window=3, center=True).median().values
    for i in range(1, len(x) - 1):
        if pd.isna(x[i]) or pd.isna(med[i]):
            continue
        if abs(x[i] - med[i]) > 5000:
            x[i] = int(med[i])
    df['totale_casi'] = x
    return df

province_df = province_df.groupby('sigla_provincia', group_keys=False).apply(smooth_anomalies)

province_df['new_cases'] = province_df.groupby('sigla_provincia')['totale_casi'].diff().clip(lower=0)
province_df['month'] = province_df['data'].dt.to_period('M').astype(str)

monthly_cases_df = province_df.groupby(['sigla_provincia', 'denominazione_provincia', 'month'], as_index=False)['new_cases'].sum()
monthly_cases_df['new_cases_sqrt'] = monthly_cases_df['new_cases'].apply(lambda x: np.sqrt(x) if x > 0 else np.nan)

max_val = monthly_cases_df['new_cases_sqrt'].max()

fig = px.choropleth_mapbox(
    monthly_cases_df,
    geojson=italy_geojson_province,
    locations='sigla_provincia',
    featureidkey='properties.prov_acr',
    color='new_cases_sqrt',
    mapbox_style="carto-positron",
    zoom=5.3,
    center=center,
    color_continuous_scale=px.colors.sequential.Sunsetdark,
    animation_frame='month',
    labels={'new_cases_sqrt': '√(New Cases)'},
    hover_name='denominazione_provincia',
    hover_data={
        'sigla_provincia': False,
        'new_cases': ':.4s',
    },
    range_color=(0, max_val)
)


fig.update_layout(
    title_text='Monthly New COVID-19 Cases by Province',
    title_x=0.5,
    title_y=0.98,
    margin={"r": 0, "t": 80, "l": 0, "b": 0},
    height=1100,
    width=880
)

fig.write_html('plots/monthly_prov_map.html')