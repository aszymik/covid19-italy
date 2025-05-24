import pandas as pd
import plotly.graph_objects as go
from pmdarima import auto_arima

# Load and preprocess data
df = pd.read_csv('data/dpc-covid19-ita-regioni.csv')
df['data'] = pd.to_datetime(df['data']).dt.date
df['totale_positivi'] = df['totale_positivi'].fillna(0)
df_daily = df.groupby('data', as_index=False)[['totale_positivi']].sum()
df_daily['data'] = pd.to_datetime(df_daily['data'])
df_daily.set_index('data', inplace=True)

# Forecast range
# train_end = '2022-05-22'
# forecast_end = '2023-05-21'

train_end = '2021-12-14'
forecast_end = '2025-01-08'

df_train = df_daily.loc[:train_end]
df_daily = df_daily.loc[:forecast_end]
forecast_steps = (pd.to_datetime(forecast_end) - df_train.index[-1]).days

# Set frequency to avoid warnings
df_train = df_train.asfreq('D')

# SARIMAX(6, 1, 1)x(1, 0, [], 7)

# Fit auto_arima model
series = df_train['totale_positivi']
print(series)
series = series.dropna()
stepwise_model = auto_arima(series,
                             seasonal=True,
                             m=7,  # weekly seasonality
                             stepwise=True,
                             suppress_warnings=True,
                             trace=True,
                             error_action='ignore',
                             max_p=10, max_q=10, max_P=3, max_Q=3,
                             d=None, D=None,  # auto-detect differencing
                             start_p=1, start_q=1,
                             start_P=0, start_Q=0)

print(stepwise_model.summary())

# Predict
forecast, conf_int = stepwise_model.predict(n_periods=forecast_steps, return_conf_int=True)

# Forecast index
forecast_index = pd.date_range(start=df_train.index[-1] + pd.Timedelta(days=1),
                               periods=forecast_steps, freq='D')

# Plot
fig = go.Figure()

# Historical (train + future observed)
fig.add_trace(go.Scatter(x=df_daily.index,
                         y=df_daily['totale_positivi'],
                         mode='lines',
                         name='Observed',
                         line=dict(color='blue')))

# Forecast
fig.add_trace(go.Scatter(x=forecast_index,
                         y=forecast,
                         mode='lines',
                         name='Forecast (auto_arima)',
                         line=dict(color='red')))

# Confidence interval
fig.add_trace(go.Scatter(
    x=forecast_index.tolist() + forecast_index[::-1].tolist(),
    y=conf_int[:, 0].tolist() + conf_int[:, 1][::-1].tolist(),
    fill='toself',
    fillcolor='rgba(255,0,0,0.2)',
    line=dict(color='rgba(255,255,255,0)'),
    hoverinfo="skip",
    showlegend=True,
    name='95% CI'
))

fig.update_layout(
    title='COVID-19 Forecast in Italy (Daily, auto_arima)',
    xaxis_title='Date',
    yaxis_title='Active Positive Cases',
    hovermode='x unified'
)

fig.write_html('plots/auto_arima_forecast.html')
fig.show()