import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Load and preprocess data
df = pd.read_csv('data/dpc-covid19-ita-regioni.csv')
df['data'] = pd.to_datetime(df['data']).dt.date
df['totale_positivi'] = df['totale_positivi'].fillna(0)
df_daily = df.groupby('data', as_index=False)[['totale_positivi']].sum()
df_daily['data'] = pd.to_datetime(df_daily['data'])
df_daily.set_index('data', inplace=True)

# Define forecast range
train_end = '2021-12-14'
forecast_end = '2025-01-08'

df_train = df_daily.loc[:train_end]
df_daily = df_daily.loc[:forecast_end]
forecast_steps = (pd.to_datetime(forecast_end) - df_train.index[-1]).days

# Set frequency to avoid warnings
df_train = df_train.asfreq('D')

# Fit SARIMAX model
model = SARIMAX(df_train['totale_positivi'],
                order=(6,1,1),              # to tune
                seasonal_order=(6,1,1,9),   # weekly seasonality
                enforce_stationarity=False,
                enforce_invertibility=False)

results = model.fit(disp=False)

# Forecast with confidence intervals
forecast = results.get_forecast(steps=forecast_steps)
forecast_index = pd.date_range(start=df_train.index[-1] + pd.Timedelta(days=1),
                               periods=forecast_steps, freq='D')

predicted_mean = forecast.predicted_mean

fig = go.Figure()

# Plot historical data
fig.add_trace(go.Scatter(
    x=df_daily.index, y=df_daily['totale_positivi'],
    mode='lines', name='Observed'
))

# Forecast
fig.add_trace(go.Scatter(
    x=forecast_index, y=predicted_mean,
    mode='lines', name='Forecast (SARIMAX)', line=dict(color='red')
))

fig.update_layout(
    title=dict(
        text='Forecast of COVID-19 Positive Cases in Italy (SARIMAX)',
        font=dict(size=24)
    ),
    xaxis=dict(
        title=dict(text='Date', font=dict(size=19)),
        tickfont=dict(size=15)
    ),
    yaxis=dict(
        title=dict(text='Number of Active Positive Cases', font=dict(size=19)),
        tickfont=dict(size=15)
    ),
    legend=dict(
        title=dict(text='Legend', font=dict(size=17)),
        font=dict(size=15)
    ),
    font=dict(size=13),
    hovermode='x unified'
)

fig.write_html('plots/sarimax.html')
