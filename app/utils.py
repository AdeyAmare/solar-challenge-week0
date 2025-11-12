import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_style("whitegrid")

def load_csv_file(uploaded_file):
    """Load CSV from uploaded file"""
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return pd.DataFrame()

def plot_boxplot(df_list, selected_names, metric):
    """Plot boxplot for uploaded datasets"""
    combined_df = pd.DataFrame()
    for df, name in zip(df_list, selected_names):
        if not df.empty and metric in df.columns:
            temp = df[[metric]].copy()
            temp['Dataset'] = name
            combined_df = pd.concat([combined_df, temp], ignore_index=True)

    if combined_df.empty:
        st.warning("No data available for the selected datasets/metric")
        return

    fig, ax = plt.subplots(figsize=(3, 3), dpi=150)  # smaller but higher-res

    sns.boxplot(x='Dataset', y=metric, data=combined_df, ax=ax)
    ax.set_title(f"{metric} Distribution")
    st.pyplot(fig)

def display_top_regions(df_list, selected_names, metric):
    """Display summary table for uploaded datasets"""
    summary = []
    for df, name in zip(df_list, selected_names):
        if not df.empty and metric in df.columns:
            summary.append({
                'Dataset': name,
                'Mean': df[metric].mean(),
                'Median': df[metric].median(),
                'Std': df[metric].std()
            })

    summary_df = pd.DataFrame(summary)
    if not summary_df.empty:
        st.subheader("Top Regions Table")
        st.dataframe(summary_df.sort_values('Mean', ascending=False).reset_index(drop=True))
