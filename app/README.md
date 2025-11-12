# Streamlit Dashboard

This folder includes an interactive Streamlit dashboard to explore solar datasets dynamically and compare metrics across regions.

# Features

CSV Uploads: Users can upload cleaned CSV files for Benin, Sierra Leone, Togo, or other regions.

Country & Metric Selection: Sidebar widgets allow selection of one or more datasets and metrics (GHI, DNI, DHI).

Interactive Boxplots: Compare distributions of selected metrics across regions.

Top Regions Table: Ranks datasets by mean value for the selected metric, highlighting the highest-potential regions.

Dynamic Updates: Visualizations and tables refresh automatically based on uploaded files and selected options.

# Usage Instructions

1. Run locally

```streamlit run app/main.py```

2. Upload CSV files using the sidebar.

3. Select countries and metric to visualize.

4. View interactive boxplots and the top regions summary table.

# Deployment

Deployed on Streamlit Community Cloud for public access.

https://solar-challenge-week0-ad78tttvmexacpilgwis9r.streamlit.app/

