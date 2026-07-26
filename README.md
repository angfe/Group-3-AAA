# AAA Team Project – Smart Mobility Analytics

**Advanced Analytics and Applications – SS 2026**
University of Cologne · Faculty of Management, Economics, and Social Sciences
Department of Information Systems for Sustainable Society

**Group 3** · Bane & Wayne Partners (BWP) Data Science Team

## How to run our code

### 1. Prerequisites

Ensure you have the following installed:

- **[Quarto](https://quarto.org/docs/get-started/)**: The publishing system used to render the report.
- **[uv](https://github.com/astral-sh/uv)**: A fast Python package manager.
- **LaTeX**: A TeX distribution (like [TinyTeX](https://yihui.org/tinytex/)) to generate the PDF.
  ```bash
  quarto install tinytex
  ```

### 2. Setup the Environment

We use `uv` to manage dependencies. Run the following commands in the root directory:

```bash

uv run python -m ipykernel install --user --name team-project-template --display-name "Group 3 Kernel"
```

This will create a `.venv` directory and register the Python kernel so Quarto can find it. You can change the `--name` if you prefer, but make sure to select the correct kernel in your editor (e.g., VS Code or Jupyter).

### 3. Rendering the Report

To generate the final report in different formats, use `uv run` to ensure Quarto uses the correct environment:

```bash
uv run quarto render report.qmd
```

This will render all formats as specified in `_quarto.yml`. If you want to render individual formats, use the `--to` argument:

- **PDF (Final Submission)**:
  ```bash
  uv run quarto render report.qmd --to pdf
  ```
- **HTML (Interactive Review)**:
  ```bash
  uv run quarto render report.qmd --to html
  ```

### 4. Configure run mode

The project supports two run modes, configured in `run_config.py`:

- **`sample`** – A reproducible, contiguous 14-day window (~291k rows) with complete weekday/weekend cycles. No API token required (uses local raw-data fallback).
- **`full`** – The complete dataset (~15M rows) from January 2024 to May 2026. Requires an API token from the [Chicago Data Portal](https://data.cityofchicago.org/).

### 5. Run notebooks in order

Run notebooks in order (`00` → `01` → `02` → `03` → `04`)

---

## Background

A renowned German car company is establishing a ride-hailing platform using a fully electrified vehicle fleet, initially targeting the US market. As the BWP Data Science Team, we are tasked with analyzing taxi trip dynamics in Chicago across temporal and spatial dimensions to support the client's operational decision-making.

Chicago taxi trip data serves as a proxy for potential ride-hailing demand.

## Data Sources

| Data Source        | Description                                                | Link                                                                                                                               |
| ------------------ | ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Taxi Data          | Chicago Taxi Trips 2024, accessed via SODA API             | [Taxi Trips 2024](https://data.cityofchicago.org/Transportation/Taxi-Trips-2024-/ajtu-isnz/about_data)                             |
| Census Tract Data  | Geographic boundaries for Chicago census tracts            | [Census Tracts](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Census_Tracts/4hp8-2i8z/about_data)                |
| Community Areas    | Geographic boundaries for Chicago community areas          | [Community Areas](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Community-Areas/igwz-8jzy/about_data) |
| Weather Data (MDW) | Hourly weather observations from Chicago Midway Airport    | [IEM ASOS](https://mesonet.agron.iastate.edu/request/download.phtml?network=IL_ASOS)                                               |
| POI Data           | Points of interest downloaded via OSMnx from OpenStreetMap | [OpenStreetMap](https://www.openstreetmap.org/)                                                                                    |
| Holidays           | US/Illinois holidays via the `holidays` Python package     | —                                                                                                                                  |

## Data Pipeline

```text
Raw CSV / Parquet (SODA API or local fallback)
   ↓
Bronze Parquet
   1:1 from CSV/API, kept as unchanged as possible
   ↓
Silver Parquet
   Cleaned, typed, and filtered data
   ↓
Gold / Features
   Merged and aggregated datasets, ML features, train/test-ready datasets
```

| Layer           | Description                                                              |
| --------------- | ------------------------------------------------------------------------ |
| Raw data        | Original API export; CSV in full mode, compressed Parquet in sample mode |
| Bronze          | One-to-one conversion from CSV/API, kept as unchanged as possible        |
| Silver          | Cleaned, typed, and filtered version of the data                         |
| Gold / Features | Feature-engineered datasets ready for ML and train/test splits           |

Spatial discretization uses H3 hexagons (resolutions 7 and 8), census tracts, and community areas. Temporal aggregation is available at 1h, 2h, 4h, and 24h intervals.

## Project Structure

```
├── 00_01_data_loader.ipynb                 # Data collection via SODA API + OSMnx POI download
├── 00_01_data_profiling.ipynb              # Bronze-level data profiling
├── 01_0x_*.ipynb                           # Data preparation (Bronze → Silver → Gold)
├── 02_0x_*.ipynb                           # Descriptive & spatial analytics, GMM hotspots
├── 03_01_predictive_analytics_baseline.ipynb
├── 03_02_*.ipynb                           # Train/validation/test split
├── 03_03_*_svm_*.ipynb                     # SVR models (community area & census tract)
├── 03_04_*_svm_classification_*.ipynb      # SVM classification and report generation
├── 03_05_*_svm_comparison.ipynb            # SVM model comparison across resolutions
├── 03_06_*_svm_nn.ipynb                    # Final NN vs. SVM comparison
├── 04_01_smart_charging_reinforcement_learning.ipynb  # RL-based EV smart charging
├── 05_*.ipynb                              # Discussion & outlook
├── run_config.py                           # Central configuration (paths, dates, run modes)
├── data/                                   # Raw, processed, and split datasets
└── models/                                 # Trained model artifacts
```

## Tasks

### 1. Data Collection and Preparation

Loading and cleaning Chicago taxi trip data via the SODA API, integrating hourly weather data from the IEM ASOS network, and downloading POI data from OpenStreetMap via OSMnx. Spatial discretization using H3 hexagons and census tracts, temporal binning at multiple resolutions (1h, 4h, 24h).

### 2. Descriptive (Spatial) Analytics

Analyzing taxi demand patterns across spatio-temporal resolutions: start times, trip lengths, start/end locations, prices, and idle times. Identifying spatial hotspots using Gaussian Mixture Models (Spatial Kernel Density Estimation).

### 3. Predictive Analytics

Predicting taxi trip demand per spatial unit and time bucket.

- **a) Support Vector Machines** – Starting with a linear kernel, progressively adding RBF and polynomial kernels. Hyperparameter tuning via grid search. Performance comparison across spatial resolutions (hexagons vs. community areas vs. census tracts).
- **b) Feedforward Neural Networks** – Repeating the prediction task with a deep learning approach and comparing against SVM results on a holdout set.

### 4. Smart Charging Using Reinforcement Learning

Designing an intelligent EV charging agent for a taxi that charges at home between 2–4 PM daily. The agent adjusts charging power every 15 minutes (0, low, medium, high) to minimize cost while ensuring sufficient energy for the next shift. The environment models stochastic energy demand (normal distribution) and an exponential cost function. Solved using tabular Q-learning with a DQN extension.

### 5. Discussion & Outlook

Interpreting results for the fleet operator, discussing implications for private vs. public charging infrastructure, and identifying further analyses and external data sources.

## Tech Stack

- **Data Processing**: pandas, polars, numpy, DuckDB
- **Spatial Analysis**: h3, geopandas, shapely, OSMnx
- **Machine Learning**: scikit-learn (SVM, GridSearchCV, StandardScaler)
- **Deep Learning**: PyTorch (DQN), TensorFlow/Keras (feedforward NN)
- **Visualization**: matplotlib, seaborn, folium
- **Configuration**: centralized via `run_config.py`
