# COVID-19 Pandemics in Italy Analysis

This project focuses on data analysis and modeling of the COVID-19 pandemic in Italy. It includes interactive visualizations, geographic insights, and time series forecasting using epidemiological and statistical models. 

## Overview

The repository contains:

- Descriptive analytics on COVID-19 cases, deaths, and hospitalizations in Italy.
- Regional and provincial analysis with interactive maps.
- Predictive modeling using:
  - **SIRS and Seasonal SIRS** epidemiological models
  - **SARIMAX** time series model

## Project Structure

```
covid19-italy/
├── data/ # Raw datasets
├── plots/ # HTML visualizations
├── scripts/ # Python scripts for analysis and modeling
```

## Visualizations

Key plots include:

- **Daily and total cases/deaths**:  
  `daily_cases.html`, `total_cases.html`, `daily_deaths.html`, `total_deaths.html`

- **Active cases and hospitalization trends**:  
  `active_cases.html`, `hospitalization.html`

- **Geographic maps**:  
  `monthly_prov_map.html`, `total_prov_map.html`, `total_prov_map_100k.html`

- **Comparison with Poland**:  
  `new_cases_vs_poland.html`

- **Cases distribution**:  
  `cases_distribution.html`, `cases_distribution_region.html`

- **Predictions**:  
  - `sirs.html`: SIRS model forecast  
  - `seasonal_sirs.html`: Seasonal SIRS model  
  - `sarimax.html`: SARIMAX time series model  

Each plot has a corresponding script generating it in the `plots/` directory.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/aszymik/covid19-italy.git
cd covid19-italy
```
2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Data sources:
* [https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv](https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv)
* [https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv](https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv)
* [https://github.com/owid/covid-19-data/blob/master/public/data/cases_deaths/weekly_cases.csv](https://github.com/owid/covid-19-data/blob/master/public/data/cases_deaths/weekly_cases.csv)
