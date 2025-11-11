import pandas as pd
import numpy as np 
import os


# --- Function to Load Data ---
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        
        # --- TIMESTAMP CONVERSION ADDED HERE ---
        if 'Timestamp' in df.columns:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            print("✅ 'Timestamp' column successfully converted to datetime objects.")
        # ---------------------------------------
            
        return df
    except FileNotFoundError:
        print(f"!!! ERROR: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during loading: {e}")
        return None

# --- Function for Summary and Missing Values ---
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

# --- Function for Z-Score Outlier Detection ---
def calculate_zscore_and_flag_outliers(df):
    """
    Flags rows as outliers if any of the key numeric columns
    (GHI, DNI, DHI, ModA, ModB, WS, WSgust) have |Z| > 3.
    Also prints the individual counts for ModA and ModB outliers.
    """
    numeric_cols = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust']
    numeric_cols = [col for col in numeric_cols if col in df.columns]

    print("🔹 Calculating Z-scores and flagging outliers for the following columns:")
    print(f"   {numeric_cols}")

    # Compute Z-scores
    zscores = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()

    # Flag rows where any Z-score exceeds 3
    df['Outliers_Flag'] = zscores.abs().gt(3).any(axis=1)
    
    if 'ModA' in zscores.columns:
        mod_a_outlier_count = zscores['ModA'].abs().gt(3).sum()
        print(f"\n📈 ModA Specific Outliers (|Z| > 3): {mod_a_outlier_count}")
    
    if 'ModB' in zscores.columns:
        mod_b_outlier_count = zscores['ModB'].abs().gt(3).sum()
        print(f"📉 ModB Specific Outliers (|Z| > 3): {mod_b_outlier_count}")
        
    # ----------------------------------------------
    
    print(f"\n✅ Total rows flagged (at least one column |Z| > 3): {df['Outliers_Flag'].sum()}")
    return df

# --- Function to Clean Outliers and Impute Missing Values ---
def clean_and_impute(df, impute_columns):
    """
    Cleans data by:
    1. Replacing flagged outliers with the median (median calculated without the outliers themselves).
    2. Imputing remaining missing values in key columns with the median.
    """

    df = df.copy()
    
    if 'Outliers_Flag' in df.columns and df['Outliers_Flag'].any():
        outlier_mask = df['Outliers_Flag']
        print("🔹 Replacing outliers with median for the following columns:")
        print(f"   {impute_columns}")
        for col in impute_columns:
            if col in df.columns:
                median_val = df.loc[~outlier_mask, col].median(skipna=True)
                df.loc[outlier_mask, col] = median_val

    # Impute any remaining missing values
    print("🔹 Imputing remaining missing values with median for key columns.")
    for col in impute_columns:
        if col in df.columns:
            median_val = df[col].median(skipna=True)
            df[col].fillna(median_val, inplace=True)

    print("✅ Outliers replaced and missing values imputed.")
    return df


# --- Function to Save Cleaned Data ---
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


