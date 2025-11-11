import pandas as pd
import numpy as np 
import os

import matplotlib.pyplot as plt
import seaborn as sns

from windrose import WindroseAxes

# Set standard styles for plots
sns.set_style("whitegrid")


# --- 1. Utility Function to Load Cleaned Data ---
def load_cleaned_data(file_path):
    """Loads the cleaned CSV file and checks for Timestamp."""
    try:
        df = pd.read_csv(file_path)
        
        # Convert Timestamp to datetime object, crucial for time series plots
        if 'Timestamp' in df.columns:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            print("✅ 'Timestamp' column converted to datetime.")
        else:
            print("⚠️ Warning: 'Timestamp' column not found.")
            
        print(f"✅ Cleaned data loaded from: {file_path}")
        return df
    except FileNotFoundError:
        print(f"!!! ERROR: Cleaned file '{file_path}' not found. Run data_preparation first.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during loading: {e}")
        return None

# --- 2. Time Series Analysis (REQUIRED) ---
import pandas as pd
import matplotlib.pyplot as plt

def plot_time_series(df):
    """
    Plots GHI, DNI, DHI, and Tamb against Timestamp using the original time resolution.
    This allows observation of patterns by month, trends throughout the day, 
    and detailed anomalies like solar peaks or rapid temperature fluctuations.
    """
    # Requirement: Check for Timestamp column
    if 'Timestamp' not in df.columns:
        print("!!! ERROR: 'Timestamp' column missing.")
        return
    
    # Ensure Timestamp is datetime for proper indexing/plotting
    try:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    except Exception as e:
        print(f"Error converting Timestamp to datetime: {e}")
        return

    # Set Timestamp as index for time series analysis
    df_ts = df.set_index('Timestamp')
    
    # Requirement: Only plot available columns (GHI, DNI, DHI, Tamb)
    # Use the raw indexed DataFrame (df_ts) for column checking
    cols_to_plot = [c for c in ['GHI', 'DNI', 'DHI', 'Tamb'] if c in df_ts.columns]
    if not cols_to_plot:
        print("!!! ERROR: None of GHI, DNI, DHI, Tamb are available.")
        return

    # Requirement: Create subplots for line charts
    fig, axes = plt.subplots(nrows=len(cols_to_plot), ncols=1, figsize=(14, 3 * len(cols_to_plot)), sharex=True)
    if len(cols_to_plot) == 1:
        axes = [axes]
    
    # Title for the overall plot
    fig.suptitle('Time Series Analysis: Raw Data', fontsize=16)

    for ax, col in zip(axes, cols_to_plot):
        # Requirement: Plot each variable vs. Timestamp
        # Plotting the original, high-resolution data for daily trends/peaks
        df_ts[col].plot(ax=ax, linewidth=0.5) 
        
        # Title on each subplot
        ax.set_title(f'{col} Over Time (Raw Data)', loc='left')
        # Y-axis label
        ax.set_ylabel(col)
        # Requirement: Show grid to help spot anomalies
        ax.grid(True, linestyle='--', alpha=0.7)
    
    # X-axis label (date)
    plt.xlabel('Date and Time') # Changed to reflect the high-resolution data
    plt.tight_layout(rect=[0,0,1,0.98])
    plt.show()




# ---  Prepare Impact Data ---
def prepare_impact_data(df_raw, df_clean):
    print("\n--- 🧑‍💻 Preparing DataFrames for Cleaning Impact Analysis ---")

    cols_to_keep = ['Timestamp', 'ModA', 'ModB']
    
    # --- Raw Data ---
    df_raw_flagged = df_raw.copy()
    if not all(col in df_raw_flagged.columns for col in cols_to_keep):
        print("!!! ERROR: Raw data is missing 'Timestamp', 'ModA', or 'ModB'. Cannot proceed.")
        return None
    
    print(f"   -> Raw data shape: {df_raw_flagged.shape}. Adding 'Cleaning = 0' flag.")
    df_raw_flagged['Cleaning'] = 0
    raw_impact_data = df_raw_flagged[cols_to_keep + ['Cleaning']]

    # --- Cleaned Data ---
    df_clean_flagged = df_clean.copy()
    if not all(col in df_clean_flagged.columns for col in cols_to_keep):
        print("!!! ERROR: Cleaned data is missing 'Timestamp', 'ModA', or 'ModB'. Cannot proceed.")
        return None
    
    print(f"   -> Cleaned data shape: {df_clean_flagged.shape}. Adding 'Cleaning = 1' flag.")
    df_clean_flagged['Cleaning'] = 1
    clean_impact_data = df_clean_flagged[cols_to_keep + ['Cleaning']]
    
    # --- Combine Raw & Cleaned ---
    df_combined = pd.concat([raw_impact_data, clean_impact_data], ignore_index=True)
    print(f"✅ Combined DataFrame created with {len(df_combined)} rows for comparison.")
    
    return df_combined

# ---  Cleaning Impact Analysis with Box Plot ---

def plot_cleaning_impact(df):
    """
    Plots the distribution of ModA & ModB grouped by Cleaning (0 = raw, 1 = cleaned) using box plots.
    """
    print("\n--- Plotting Cleaning Impact Analysis ---")

    required_cols = ['ModA', 'ModB', 'Cleaning']
    if not all(col in df.columns for col in required_cols):
        print("!!! ERROR: Missing one or more required columns: 'ModA', 'ModB', 'Cleaning'.")
        return

    # Print average values for reference
    grouped_avg = df.groupby('Cleaning', as_index=False)[['ModA', 'ModB']].mean()
    print("\nAverage Values by Cleaning Flag:\n", grouped_avg.set_index('Cleaning'))

    # Box Plots
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Distribution of ModA & ModB by Cleaning Flag', fontsize=16)

    # ModA Box Plot
    sns.boxplot(x='Cleaning', y='ModA', data=df, hue='Cleaning', palette=['skyblue', 'orange'], legend=False, ax=axes[0])
    axes[0].set_title('ModA Distribution')
    axes[0].set_xticks([0, 1])
    axes[0].set_xticklabels(['Not Cleaned', 'Cleaned'])
    axes[0].set_ylabel('ModA Value')
    axes[0].set_xlabel('Cleaning Flag')

    # ModB Box Plot
    sns.boxplot(x='Cleaning', y='ModB', data=df, hue='Cleaning', palette=['skyblue', 'orange'], legend=False, ax=axes[1])
    axes[1].set_title('ModB Distribution')
    axes[1].set_xticks([0, 1])
    axes[1].set_xticklabels(['Not Cleaned', 'Cleaned'])
    axes[1].set_ylabel('ModB Value')
    axes[1].set_xlabel('Cleaning Flag')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

# --- 4. Correlation & Relationship Analysis (REQUIRED) ---
def plot_correlation_heatmap(df):
    """Heatmap of correlations for GHI, DNI, DHI, TModA, and TModB."""
    print("\n--- Plotting Correlation Heatmap ---")
    
    corr_cols = ['GHI', 'DNI', 'DHI', 'TModA', 'TModB']
    
    # Ensure columns exist
    available_cols = [col for col in corr_cols if col in df.columns]
    if len(available_cols) < 2:
        print("!!! ERROR: Not enough columns available for correlation heatmap.")
        return
        
    corr_matrix = df[available_cols].corr()
    
    plt.figure(figsize=(8, 7))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.show()

def plot_scatter_relationships(df):
    """
    Scatter plots: WS, WSgust, WD vs. GHI; RH vs. Tamb; RH vs. GHI.
    Uses a sample of the data for plotting to avoid overplotting.
    """
    print("\n--- Plotting Relationship Scatter Plots ---")
    
    # Define all required (x, y) pairs
    pairs = [('WS', 'GHI'), ('WSgust', 'GHI'), ('WD', 'GHI'), 
             ('RH', 'Tamb'), ('RH', 'GHI')]
    
    # Check which pairs are possible
    available_pairs = []
    for x_col, y_col in pairs:
        if x_col in df.columns and y_col in df.columns:
            available_pairs.append((x_col, y_col))
        else:
            print(f"Skipping scatter plot: Columns '{x_col}' or '{y_col}' not found.")
            
    if not available_pairs:
        print("!!! ERROR: No available pairs for scatter plots.")
        return

    # Use a sample of the data if it's large to prevent overplotting
    sample_size = min(5000, len(df))
    df_sample = df.sample(n=sample_size, random_state=1)

    # Adjust grid size based on number of plots
    num_plots = len(available_pairs)
    num_cols = 2
    num_rows = (num_plots + num_cols - 1) // num_cols # Calculate rows needed
    
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(14, 6 * num_rows))
    fig.suptitle('Relationship Analysis (Sampled Data)', fontsize=16)
    
    # Flatten axes for easy iteration
    axes = axes.flatten()

    for i, (x_col, y_col) in enumerate(available_pairs):
        sns.scatterplot(data=df_sample, x=x_col, y=y_col, ax=axes[i], alpha=0.6, s=10)
        axes[i].set_title(f'{y_col} vs. {x_col}')
    
    # Hide any unused subplots
    for j in range(num_plots, len(axes)):
        fig.delaxes(axes[j])
            
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.show()

# --- 5. Wind & Distribution Analysis (REQUIRED) ---
def plot_wind_and_distribution(df):
    """Histograms for GHI and WS, and a wind rose for WS/WD."""
    print("\n--- Plotting Distribution Histograms ---")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Histogram for GHI
    if 'GHI' in df.columns:
        sns.histplot(df['GHI'], kde=True, bins=50, ax=axes[0])
        axes[0].set_title('Distribution of GHI')
    else:
        axes[0].set_title('GHI Column Not Found')

    # Histogram for WS
    if 'WS' in df.columns:
        sns.histplot(df['WS'], kde=True, bins=30, ax=axes[1])
        axes[1].set_title('Distribution of Wind Speed (WS)')
    else:
        axes[1].set_title('WS Column Not Found')
        
    plt.tight_layout()
    plt.show()
    
    # --- Wind Rose ---
    if 'WS' in df.columns and 'WD' in df.columns:
        print("\n--- Plotting Wind Rose ---")
        try:
            plt.figure(figsize=(8, 8))
            ax = WindroseAxes.from_ax()
            # Clean data: drop NaNs in WS/WD for the plot
            wind_df = df[['WD', 'WS']].dropna()
            ax.bar(wind_df['WD'], wind_df['WS'], normed=True, opening=0.8, edgecolor='white')
            ax.set_legend(title="Wind Speed (m/s)")
            plt.title('Wind Rose (Wind Direction and Speed)')
            plt.show()
        except Exception as e:
            print(f"!!! ERROR: Could not generate Wind Rose. {e}")
    else:
        print("Skipping Wind Rose: 'WS' or 'WD' columns not found.")

# --- 6. Bubble Chart (REQUIRED) ---
def plot_bubble_chart(df):
    """
    Bubble chart of GHI vs. Tamb, with bubble size = RH.
    Addresses the 'Temperature Analysis' requirement.
    Uses a sample of the data for plotting.
    """
    print("\n--- Plotting Bubble Chart (GHI vs. Tamb, Size = RH) ---")
    
    required_cols = ['GHI', 'Tamb', 'RH']
    if not all(col in df.columns for col in required_cols):
        print("!!! ERROR: Missing one or more required columns: 'GHI', 'Tamb', 'RH'.")
        return

    # Use a sample for performance
    sample_size = min(5000, len(df))
    df_sample = df.sample(n=sample_size, random_state=1)
    
    plt.figure(figsize=(12, 8))
    
    # Normalize RH for bubble size (e.g., from 10 to 500)
    if df_sample['RH'].max() > 0:
        size = (df_sample['RH'] / df_sample['RH'].max()) * 500
        size = size.fillna(10) # Handle potential NaNs
    else:
        size = 50 # Default size if RH max is 0

    scatter = plt.scatter(data=df_sample, x='Tamb', y='GHI', 
                          s=size, c='RH', 
                          cmap='viridis', alpha=0.6, 
                          edgecolors='w', linewidth=0.5)
    
    plt.xlabel('Ambient Temperature (Tamb)')
    plt.ylabel('Global Horizontal Irradiance (GHI)')
    plt.title('GHI vs. Tamb (Bubble Size = Relative Humidity, RH)')
    
    # Add a color bar to show what the color means
    plt.colorbar(scatter, label='Relative Humidity (RH)')
    
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

