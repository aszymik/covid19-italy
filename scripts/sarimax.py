import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Load and preprocess data
df = pd.read_csv('data/dpc-covid19-ita-regioni.csv')
df['data'] = pd.to_datetime(df['data'])
df_daily = df.groupby('data', as_index=False)[['totale_positivi']].sum()
df_daily.set_index('data', inplace=True)

# Filter training data up to end of 2021
train_end = '2022-03-07'
df_train = df_daily.loc[:train_end]

# Set explicit frequency to avoid warnings
df_train = df_train.asfreq('D')

# Define forecast range
forecast_end = '2025-01-08'
forecast_steps = (pd.to_datetime(forecast_end) - df_train.index[-1]).days

# Fit SARIMAX model
model = SARIMAX(df_train['totale_positivi'],
                order=(15,7,7),              # you can tune this
                seasonal_order=(15,7,7,60),   # weekly seasonality
                enforce_stationarity=False,
                enforce_invertibility=False)

results = model.fit(disp=False)

# Forecast with confidence intervals
forecast = results.get_forecast(steps=forecast_steps)
forecast_index = pd.date_range(start=df_train.index[-1] + pd.Timedelta(days=1),
                               periods=forecast_steps, freq='D')

predicted_mean = forecast.predicted_mean
conf_int = forecast.conf_int()

# Plot
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

# Confidence interval
fig.add_trace(go.Scatter(
    x=forecast_index.tolist() + forecast_index[::-1].tolist(),
    y=conf_int.iloc[:, 0].tolist() + conf_int.iloc[:, 1][::-1].tolist(),
    fill='toself',
    fillcolor='rgba(255,0,0,0.2)',
    line=dict(color='rgba(255,255,255,0)'),
    hoverinfo="skip",
    showlegend=True,
    name='95% CI'
))

# Layout
fig.update_layout(
    title='Forecast of COVID-19 Positive Cases in Italy (SARIMAX)',
    xaxis_title='Date',
    yaxis_title='Number of Active Positive Cases',
    legend_title='Legend',
    hovermode='x unified',
)

fig.write_html('plots/sarimax.html')
fig.show()
