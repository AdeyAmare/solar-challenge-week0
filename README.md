# KAIM-Week-0: Solar Challenge
This project explores solar energy potential across Benin, Sierra Leone, and Togo. It covers data profiling, cleaning, exploratory analysis, and cross-country comparisons using provided datasets. The goal is to provide actionable insights on solar energy availability in these regions.

# Project Structure
```
solar-challenge-week0/
├── .github/                # GitHub Actions workflows
├── data/                   # Cleaned CSV datasets (ignored by Git)
├── notebooks/              # Jupyter notebooks for EDA and comparisons
│   ├── benin_eda.ipynb
│   ├── sierra_leone_eda.ipynb
│   ├── togo_eda.ipynb
│   └── compare_countries.ipynb
├── scripts/                # Modular Python scripts
│   ├── file_loading_handler.py   # Base class for data loading
│   ├── data_prep_clean.py        # Dataset cleaning and profiling
│   ├── eda_plots.py              # EDA visualizations
│   └── compare_countries.py      # Cross-country comparison
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


4. Modular & Reproducible Design

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

The cross-country comparison notebook loads cleaned CSV files using ComparisonHandler, visualizes distributions of GHI, DNI, and DHI with boxplots, computes summary statistics and averages, performs ANOVA and Kruskal–Wallis tests to assess statistical differences between countries, and generates bar charts ranking countries by average GHI to highlight regions with the highest solar potential.

### Note

All scripts can be imported in notebooks for step-by-step execution or experimentation.

# Branching Strategy

```main``` — Protected branch for final versions.

```setup-task``` — Environment setup.

```eda-benin, eda-sierraleone, eda-togo``` — Individual country EDA.

```compare-countries``` — Cross-country analysis.