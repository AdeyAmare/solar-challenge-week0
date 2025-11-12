# KAIM-Week-0: Solar Challenge
This project explores solar energy potential across Benin, Sierra Leone, and Togo. It covers data profiling, cleaning, exploratory analysis, and cross-country comparisons using provided datasets. The goal is to provide actionable insights on solar energy availability in these regions.

# Project Structure
```
solar-challenge-week0/
├── .github/                  # GitHub Actions workflows
├── app/                      # Streamlit app for interactive dashboard
│   ├── __init__.py
│   ├── main.py
│   ├── utils.py
│   └── README.md
├── dashboard_screenshots/                     # Interactive Dashboard Screenshots
├── data/                     # Cleaned CSV datasets (ignored by Git)
├── src/
│   ├── notebooks/            # Jupyter notebooks for EDA and comparisons
│   │   ├── __init__.py
│   │   ├── benin_eda.ipynb
│   │   ├── sierra_leone_eda.ipynb
│   │   ├── togo_eda.ipynb
│   │   ├── compare_countries.ipynb
│   │   └── README.md
├── scripts/                  # Modular Python scripts
│   ├── __init__.py
│   ├── file_loading_handler.py   # Base class for data loading
│   ├── data_prep_clean.py        # Dataset cleaning and profiling
│   ├── eda_plots.py              # EDA visualizations
│   └── compare_countries.py      # Cross-country comparison
│   └── README.md
├── .gitignore
├── requirements.txt
└── README.md

```


# Key Features
1. Data Loading & Cleaning

The `DatasetHandler` class loads CSV datasets and formats the Timestamp column. It detects outliers using Z-scores, replaces them with median values, and imputes missing values to maintain dataset integrity. Cleaned data is then saved to country-specific folders within the `data/` directory.


2. Exploratory Data Analysis (EDA)

The `EDAHandler` class generates visualizations to explore solar patterns, including time series, cleaning impact plots, correlation heatmaps, scatter/bubble charts, and wind rose diagrams.

3. Cross-Country Comparison

The `ComparisonHandler` class combines cleaned datasets across countries, generating boxplots and average GHI bar charts, and performs ANOVA and Kruskal–Wallis tests to assess differences in solar irradiance.

5. Interactive Dashboard

The Streamlit dashboard allows users to upload CSV files, select countries and metrics, visualize interactive boxplots, and view top regions tables. It provides a dynamic interface for exploring solar data insights and is ready for deployment on Streamlit Community Cloud.

6. Modular & Reproducible Design

Core functionality is implemented in Python classes under scripts/ to maintain reusable, clean code. Notebooks focus on analysis and storytelling, keeping complex logic separate.

# Reproducing the Environment

1. Clone the project from GitHub (replace <your-username> with your actual GitHub username):
   
```
git clone https://github.com/<your-username>/solar-challenge-week0.git

cd solar-challenge-week0
```

2. Create and Activate the Virtual Environment
   
- Create the venv:
```
python -m venv .venv
```

- Activate the venv
```
.venv\Scripts\activate
```
3. Install Dependencies
```
pip install -r requirements.txt
```
4. CI Workflow

A GitHub Actions workflow is set up in .github/workflows/ci.yml to automatically run ```pip install -r requirements.txt``` and verify the Python version on every push and pull request.

# Usage

### Run the EDA notebooks for each country to explore raw and cleaned data.

Each country has a dedicated notebook to explore raw and cleaned data:

```benin_eda.ipynb``` – Exploratory analysis for Benin.

```sierra_leone_eda.ipynb``` – Exploratory analysis for Sierra Leone.

```togo_eda.ipynb``` – Exploratory analysis for Togo.

Each notebook demonstrates the full data workflow: loading raw datasets with DatasetHandler, generating summary reports and detecting outliers, cleaning and imputing missing values, and visualizing key patterns through time series, scatter plots, correlation heatmaps, wind rose diagrams, and bubble charts.


### Use ```compare_countries.ipynb``` to analyze solar potential across Benin, Sierra Leone, and Togo.

The cross-country comparison notebook loads cleaned CSVs, visualizes GHI, DNI, and DHI distributions with boxplots, computes summary statistics, performs ANOVA/Kruskal–Wallis tests, and ranks countries by average GHI to highlight top solar regions.


### Use `app/main.py` to explore solar datasets interactively.

The Streamlit dashboard lets users upload CSVs, select countries and metrics, view interactive boxplots, and see a top regions table ranking solar potential in real time.

### Note

All scripts can be imported in notebooks for step-by-step execution or experimentation.

# Branching Strategy

```main``` — Protected branch for final versions.

```setup-task``` — Environment setup.

```eda-benin, eda-sierraleone, eda-togo``` — Individual country EDA.

```compare-countries``` — Cross-country analysis.

```dashboard-dev``` —    Interactive Dashboard