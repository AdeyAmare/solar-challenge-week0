import streamlit as st
from utils import load_csv_file, plot_boxplot, display_top_regions

st.set_page_config(page_title="Solar Dashboard", layout="wide")
st.title("☀️ Solar Energy Dashboard")
st.write("Upload your CSV files, select datasets and metrics, and view boxplots and top regions.")

# --- Sidebar: metric selection ---
metric_options = ["GHI", "DNI", "DHI"]
metric = st.sidebar.selectbox("Select Metric", metric_options)

# --- File uploads ---
st.sidebar.header("Upload CSV Files")
uploaded_files = st.sidebar.file_uploader(
    "Upload CSVs (one per country/dataset)", type="csv", accept_multiple_files=True
)

if uploaded_files:
    dataset_names = [f.name for f in uploaded_files]
    # Optionally allow user to select which uploaded datasets to include
    selected_names = st.sidebar.multiselect(
        "Select Datasets to Include", dataset_names, default=dataset_names
    )

    # Load the selected files
    dfs = [load_csv_file(f) for f in uploaded_files if f.name in selected_names]

    # --- Boxplot ---
    st.subheader(f"Boxplot of {metric}")
    plot_boxplot(dfs, selected_names, metric)

    st.markdown("---")

    # --- Top regions table ---
    display_top_regions(dfs, selected_names, metric)

    st.markdown("---")
    st.caption("Built by Adey Amare")
else:
    st.info("Please upload at least one CSV file to visualize data.")
