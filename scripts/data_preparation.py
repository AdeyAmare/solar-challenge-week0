import pandas as pd
import numpy as np 
import os

# --- 2. Function to Load Data ---
def load_data(file_path):
    try:
        df = pd.read_csv(file_path, parse_dates=['Timestamp'])
        return df
    except FileNotFoundError:
        print(f"!!! ERROR: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during loading: {e}")
        return None

# --- 3. Function for Summary and Missing Values ---
def get_summary_report(df):
    """Prints required summary statistics and missing value reports."""
    print("\n--- 1. Summary Statistics ---")
    print(df.describe())
    
    missing_counts = df.isna().sum()
    print("\n--- 2. Missing Value Report ---")
    print(missing_counts)
    
    # List columns with >5% nulls
    total_rows = len(df)
    missing_percent = (missing_counts / total_rows) * 100
    high_null_cols = missing_percent[missing_percent > 5]
    
    print("\n--- 3. Columns with >5% Missing Values ---")
    if high_null_cols.empty:
        print("No columns have more than 5% missing values.")
    else:
        print(high_null_cols)

# --- 4. Function for Z-Score Outlier Detection ---
def calculate_zscore_and_flag_outliers(df):
    REQUIRED_COLS = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust']
    
    # Select only the required columns that exist
    cols_for_zscore = [col for col in REQUIRED_COLS if col in df.columns]
    df_for_zscore = df[cols_for_zscore].copy()
    
    if df_for_zscore.empty:
        df['Outliers_Flag'] = False
        return df

    # Calculate Z-scores: (Value - Mean) / Standard Deviation
    df_zscores = (df_for_zscore - df_for_zscore.mean()) / df_for_zscore.std()
    
    # Flag rows with |Z| > 3
    outliers = df_zscores.abs() > 3
    df['Outliers_Flag'] = outliers.any(axis=1)
    
    return df

# --- 5. Function to Clean Outliers and Missing Values ---
def clean_and_impute(df, impute_columns):
    """Cleans data by replacing flagged outliers and remaining NaNs with the median."""
    
    # Step 5a: Replace Flagged Outliers with Median
    if 'Outliers_Flag' in df.columns and df['Outliers_Flag'].any():
        outlier_mask = df['Outliers_Flag']
        
        for col in impute_columns:
            if col in df.columns:
                median_val = df[col].median()
                df.loc[outlier_mask, col] = median_val

    # Step 5b: Impute Remaining Missing Values with Median
    for col in impute_columns:
        if col in df.columns:
            median_value = df[col].median(skipna=True)
            df[col].fillna(median_value, inplace=True)
            
    return df

# --- 6. Function to Save Cleaned Data ---
def save_cleaned_data(df, output_path):
    """Exports the cleaned DataFrame to a new CSV file."""
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    try:
        # Remove the temporary flag column before saving
        if 'Outliers_Flag' in df.columns:
            df = df.drop(columns=['Outliers_Flag'])
            
        df.to_csv(output_path, index=False)
        print(f"\n✅ Cleaned Data Saved successfully to: {output_path}")
    except Exception as e:
        print(f"!!! ERROR: Could not save file. {e}")
