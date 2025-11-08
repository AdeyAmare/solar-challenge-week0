# scripts/data_analysis_notebook.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from windrose import WindroseAxes  # for wind rose plotting

# Set standard styles for plots
sns.set_style("whitegrid")

# --- 1. Utility Function to Load Cleaned Data ---
def load_cleaned_data(file_path):
    """Loads the cleaned CSV file and sets Timestamp as index."""
    try:
        df = pd.read_csv(file_path, parse_dates=['Timestamp'], index_col='Timestamp')
        print(f"\n✅ Cleaned data loaded from: {file_path}")
        return df
    except FileNotFoundError:
        print(f"!!! ERROR: Cleaned file '{file_path}' not found. Run data_preparation first.")
        return None

# --- 2. Time Series Analysis (REQUIRED) ---
def plot_time_series(df):
    """Line or bar charts of GHI, DNI, DHI, Tamb vs. Timestamp."""
    time_series_cols = ['GHI', 'DNI', 'DHI', 'Tamb']
    fig, axes = plt.subplots(nrows=len(time_series_cols), ncols=1, figsize=(14, 3 * len(time_series_cols)), sharex=True)
    fig.suptitle('Time Series Analysis: GHI, DNI, DHI, and Ambient Temperature', fontsize=16)

    for i, col in enumerate(time_series_cols):
        if col in df.columns:
            df[col].plot(ax=axes[i], legend=False)
            axes[i].set_title(f'{col} Over Time', loc='left')
            axes[i].set_ylabel(col)
            axes[i].grid(True, linestyle='--', alpha=0.7)
            
    plt.xlabel('Timestamp')
    plt.tight_layout(rect=[0, 0, 1, 0.98]) 
    plt.show()

# --- 3. Cleaning Impact Analysis (REQUIRED) ---
def plot_cleaning_impact(input_raw_path, cleaned_df):
    """
    Plots the distribution of ModA and ModB pre/post-clean (requires loading raw data).
    """
    print("\n--- Plotting Cleaning Impact (ModA & ModB Pre/Post-Clean) ---")
    
    try:
        raw_file_path = input_raw_path.replace('_clean.csv', '.csv')
        raw_df = pd.read_csv(raw_file_path, parse_dates=['Timestamp'], index_col='Timestamp')
    except Exception as e:
        print(f"!!! WARNING: Could not load raw data from {raw_file_path}. Skipping Cleaning Impact plot.")
        return

    columns = ['ModA', 'ModB']
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Distribution Impact of Outlier Cleaning on Sensor Readings', fontsize=16)

    for i, col in enumerate(columns):
        if col in raw_df.columns and col in cleaned_df.columns:
            sns.kdeplot(raw_df[col].resample('D').mean().dropna(), ax=axes[i], label='Raw (Pre-Clean)', linewidth=2)
            sns.kdeplot(cleaned_df[col].resample('D').mean().dropna(), ax=axes[i], label='Cleaned (Post-Clean)', linewidth=2)
            axes[i].set_title(f'Distribution of Daily Average {col}')
            axes[i].legend()

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

# --- 4. Correlation & Relationship Analysis (REQUIRED) ---
def plot_correlation_heatmap(df):
    """Heatmap of correlations (GHI, DNI, DHI, TModA, TModB)."""
    print("\n--- Plotting Correlation Heatmap ---")
    corr_cols = ['GHI', 'DNI', 'DHI', 'TModA', 'TModB']
    corr_matrix = df[corr_cols].corr()
    
    plt.figure(figsize=(8, 7))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title('Correlation Heatmap of Solar Irradiance and Module Temperatures')
    plt.tight_layout()
    plt.show()

def plot_scatter_relationships(df):
    """Scatter plots: WS, WSgust, WD vs. GHI; RH vs. Tamb or RH vs. GHI."""
    print("\n--- Plotting Relationship Scatter Plots ---")
    pairs = [('WS', 'GHI'), ('WSgust', 'GHI'), ('RH', 'Tamb'), ('RH', 'GHI')]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle('Relationship Analysis', fontsize=16)
    axes = axes.flatten()

    for i, (x_col, y_col) in enumerate(pairs):
        if x_col in df.columns and y_col in df.columns:
            sns.scatterplot(x=df[x_col], y=df[y_col], ax=axes[i], alpha=0.6, s=10)
            axes[i].set_title(f'{y_col} vs. {x_col}')
        
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

# --- 5. Wind & Distribution Analysis (REQUIRED) ---
def plot_wind_and_distribution(df):
    """Histograms for GHI, WS and wind rose for WS/WD."""
    print("\n--- Plotting Distribution Histograms ---")
    
    # Histogram for GHI
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    sns.histplot(df['GHI'], kde=True, bins=50)
    plt.title('Distribution of GHI')

    # Histogram for WS
    plt.subplot(1, 2, 2)
    sns.histplot(df['WS'], kde=True, bins=30)
    plt.title('Distribution of Wind Speed (WS)')
    plt.tight_layout()
    plt.show()
    
    # Wind Rose
    if 'WS' in df.columns and 'WD' in df.columns:
        print("\n--- Plotting Wind Rose ---")
        plt.figure(figsize=(8, 8))
        ax = WindroseAxes.from_ax()
        ax.bar(df['WD'], df['WS'], normed=True, opening=0.8, edgecolor='white')
        ax.set_legend(title="Wind Speed (m/s)")
        plt.show()

# --- 6. Bubble Chart (REQUIRED) ---
def plot_bubble_chart(df):
    """GHI vs. Tamb with bubble size = RH."""
    print("\n--- Plotting Bubble Chart (GHI vs. Tamb) ---")
    plt.figure(figsize=(10, 8))
    
    size = df['RH'] / df['RH'].max() * 500
    scatter = plt.scatter(x=df['Tamb'], y=df['GHI'], s=size, c=df['RH'], 
                          cmap='viridis', alpha=0.6, edgecolors='w', linewidth=0.5)
    
    plt.xlabel('Ambient Temperature (Tamb)')
    plt.ylabel('Global Horizontal Irradiance (GHI)')
    plt.title('GHI vs. Tamb (Bubble Size = Relative Humidity, RH)')
    plt.colorbar(scatter, label='Relative Humidity (RH)')
    plt.tight_layout()
    plt.show()
