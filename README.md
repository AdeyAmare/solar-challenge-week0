# KAIM-Week-0: Solar Challenge

# Task 1: Git & Environment Setup Overview

This repository was initialized to fulfill the environment setup and version control requirements for the KIAM-Week-0 challenge.

# Key Deliverables

- Repository Initialization: Created and cloned the solar-challenge-week0 repository.

- Virtual Environment: Set up a Python virtual environment (venv).

- Version Control: Implemented .gitignore, requirements.txt, and committed changes on a dedicated branch (setup-task).

- Continuous Integration (CI): Added a GitHub Actions workflow (.github/workflows/ci.yml) to ensure dependency installation is working.

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

# Task 2: Solar Data Analysis

This task covers preparing, cleaning, and analyzing solar datasets for multiple countries using reusable scripts.

## Key Steps

## Data Preparation: 
Load raw data, inspect missing values, detect outliers, clean/impute anomalies, and save cleaned datasets.

## Data Analysis:
Time series plots for GHI, DNI, DHI, and temperature.
Cleaning impact plots for sensor readings.
Correlation heatmaps and scatter plots for variable relationships.
Wind and distribution analysis with histograms and wind rose plots.
Bubble charts showing GHI vs. temperature with relative humidity as bubble size.

Note: All steps use modular scripts in the scripts folder, making the workflow reusable for different datasets.

## Running Task 2

Ensure dependencies are installed as per Task 1.
Run the notebooks for each country to execute the full preparation and analysis workflow using the scripts.
Users should have a data/ folder in the project root containing the raw CSVs, or check the notebook code for the expected folder structure.

