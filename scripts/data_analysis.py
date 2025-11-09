import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# The 'windrose' library is required for the wind rose plot.
# You may need to install it first (e.g., using 'pip install windrose')
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
def plot_time_series(df):
    """
    Plots GHI, DNI, DHI, and Tamb against the Timestamp.
    Resamples to daily averages for a clearer, high-level view.
    """
    print("\n--- Plotting Time Series Analysis (Daily Averages) ---")
    
    # Ensure Timestamp is the index for resampling
    if 'Timestamp' not in df.columns:
        print("!!! ERROR: 'Timestamp' column missing for time series analysis.")
        return
        
    df_ts = df.set_index('Timestamp')
    
    # Resample to Daily ('D') averages to make the plot readable
    # For a more detailed plot, you could use 'H' (hourly) or plot a small slice
    try:
        df_daily = df_ts.resample('D').mean(numeric_only=True)
    except Exception as e:
        print(f"Error during resampling: {e}")
        return

    time_series_cols = ['GHI', 'DNI', 'DHI', 'Tamb']
    
    # Check which columns are available in the resampled data
    available_cols = [col for col in time_series_cols if col in df_daily.columns]
    
    if not available_cols:
        print("!!! ERROR: None of the required time series columns (GHI, DNI, DHI, Tamb) are available.")
        return

    # Create stacked subplots
    fig, axes = plt.subplots(nrows=len(available_cols), ncols=1, figsize=(14, 3 * len(available_cols)), sharex=True)
    
    # Handle the case of a single plot (axes is not an array)
    if len(available_cols) == 1:
        axes = [axes]
        
    fig.suptitle('Time Series Analysis: Daily Averages', fontsize=16)

    for i, col in enumerate(available_cols):
        df_daily[col].plot(ax=axes[i], legend=False)
        axes[i].set_title(f'{col} Over Time', loc='left')
        axes[i].set_ylabel(col)
        axes[i].grid(True, linestyle='--', alpha=0.7)
        
    plt.xlabel('Date')
    plt.tight_layout(rect=[0, 0, 1, 0.98]) 
    plt.show()

# --- 3. Cleaning Impact Analysis (REQUIRED) ---
# --- 3. Cleaning Impact Analysis (REQUIRED) ---
def plot_cleaning_impact(df):
    """
    Plots average ModA & ModB grouped by Cleaning (0 = raw, 1 = cleaned).
    """
    print("\n--- Plotting Cleaning Impact Analysis ---")

    required_cols = ['ModA', 'ModB', 'Cleaning']
    if not all(col in df.columns for col in required_cols):
        print("!!! ERROR: Missing one or more required columns: 'ModA', 'ModB', 'Cleaning'.")
        return

    # Group by 'Cleaning' and calculate the mean. 
    # as_index=False makes 'Cleaning' a regular column, which is easier for seaborn.
    grouped_avg = df.groupby('Cleaning', as_index=False)[['ModA', 'ModB']].mean()
    print("\nAverage Values by Cleaning Flag:\n", grouped_avg.set_index('Cleaning'))
    # --------------------------------------

    # Bar Plot for grouped averages
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Average ModA & ModB by Cleaning Flag', fontsize=16)

    # Define custom labels that will be used for both plots
    custom_labels = ['Not Cleaned (0)', 'Cleaned (1)']

    # Use 'data', 'x', and 'y' parameters for simplicity.
    sns.barplot(x='Cleaning', y='ModA', data=grouped_avg, ax=axes[0], color='skyblue')
    axes[0].set_title('Average ModA')
    axes[0].set_ylabel('Average ModA Value')
    
    axes[0].set_xticks([0, 1])
    axes[0].set_xticklabels(custom_labels)
    axes[0].set_xlabel('Cleaning Flag') # Clearer X label

    sns.barplot(x='Cleaning', y='ModB', data=grouped_avg, ax=axes[1], color='orange')
    axes[1].set_title('Average ModB')
    axes[1].set_ylabel('Average ModB Value')
    
    axes[1].set_xticks([0, 1])
    axes[1].set_xticklabels(custom_labels)
    axes[1].set_xlabel('Cleaning Flag') # Clearer X label

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

