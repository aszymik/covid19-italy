import pandas as pd
import numpy as np
from scipy.integrate import odeint
import plotly.graph_objects as go

df = pd.read_csv('data/dpc-covid19-ita-regioni.csv')
df['data'] = pd.to_datetime(df['data'])
df_daily = df.groupby('data', as_index=False)[['totale_positivi', 'dimessi_guariti']].sum()

# Filter data to the beginning of third wave
start_date = '2021-10-27'
end_date = '2025-01-08'
mask = (df_daily['data'] >= start_date) & (df_daily['data'] <= end_date)
df_wave3 = df_daily.loc[mask].copy()
days = (df_wave3['data'] - pd.to_datetime(start_date)).dt.days.to_numpy()

# Seasonal SIRS model
def seasonal_sirs_model(y, t, beta0, gamma, delta, alpha, period):
    S, I, R = y
    N = S + I + R
    beta_t = beta0 * (1 + alpha * np.cos(2 * np.pi * t / period))
    dSdt = -beta_t * S * I / N + delta * R
    dIdt = beta_t * S * I / N - gamma * I
    dRdt = gamma * I - delta * R
    return [dSdt, dIdt, dRdt]

beta = 0.28     # infection rate
gamma = 0.21    # recovery rate
delta = 0.01    # rate of  immunity loss
alpha = 0.1     # amplitude of seasonal fluctuation
period = 365

# Initial conditions
N = 60_000_000  # approximate Italy population
I0 = df_wave3['totale_positivi'].iloc[0]
R0 = df_wave3['dimessi_guariti'].iloc[0]

S0 = N - I0 - R0
y0 = [S0, I0, R0]
t = np.arange(0, len(df_wave3))

# Solve equation
sol = odeint(seasonal_sirs_model, y0, t, args=(beta, gamma, delta, alpha, period))
S, I, R = sol.T

# Plot
fig = go.Figure()

# Real daily new cases (full timeline)
fig.add_trace(go.Scatter(
    x=df_daily['data'], y=df_daily['totale_positivi'],
    mode='lines', name='Real'
))

# Predicted infections (SIRS model, third wave only)
fig.add_trace(go.Scatter(
    x=df_wave3['data'], y=I,
    mode='lines', name='Predicted'
))

# Layout and style
fig.update_layout(
    title='COVID-19 in Italy: Seasonal SIRS Model Predictions',
    xaxis_title='Date',
    yaxis_title='Number of Infected People',
    legend_title='Legend',
    hovermode='x unified'
)

fig.write_html('plots/seasonal_sirs.html')