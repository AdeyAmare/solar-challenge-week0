import pandas as pd
import numpy as np
import os

from file_loading_handler import FileLoadingHandler

class DatasetHandler(FileLoadingHandler):
    """
    Class for handling dataset operations: summarizing, 
    detecting outliers, cleaning/imputing, and saving.
    """

    def get_summary_report(self):
        """
        Print a summary report including:
        - Descriptive statistics
        - Missing value counts
        - Columns with more than 5% missing values
        """
        df = self.df
        if df is None:
            print("!!! ERROR: No data loaded.")
            return
        
        print("\n--- 1. Summary Statistics ---")
        print(df.describe())
        
        # Count missing values per column
        missing_counts = df.isna().sum()
        print("\n--- 2. Missing Value Report ---")
        print(missing_counts)
        
        # Highlight columns with >5% missing
        total_rows = len(df)
        missing_percent = (missing_counts / total_rows) * 100
        high_null_cols = missing_percent[missing_percent > 5]
        
        print("\n--- 3. Columns with >5% Missing Values ---")
        if high_null_cols.empty:
            print("No columns have more than 5% missing values.")
        else:
            print(high_null_cols)

    def calculate_zscore_and_flag_outliers(self):
        """
        Calculate Z-scores for numeric columns and flag rows with any |Z| > 3 as outliers.
        Updates the DataFrame with a new 'Outliers_Flag' column.

        Returns:
        --------
        pd.DataFrame or None
            DataFrame with outliers flagged or None if no data loaded.
        """
        df = self.df
        if df is None:
            print("!!! ERROR: No data loaded.")
            return None
        
        # List of numeric columns to check
        numeric_cols = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust']
        numeric_cols = [col for col in numeric_cols if col in df.columns]

        print("🔹 Calculating Z-scores and flagging outliers for the following columns:")
        print(f"   {numeric_cols}")

        # Compute Z-scores
        zscores = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()

        # Flag rows where any Z-score > 3
        df['Outliers_Flag'] = zscores.abs().gt(3).any(axis=1)
        
            
        print(f"\n✅ Total rows flagged (at least one column |Z| > 3): {df['Outliers_Flag'].sum()}")
        self.df = df
        return df

    def clean_and_impute(self, impute_columns):
        """
        Replace outliers with median and impute missing values in specified columns.

        Parameters:
        -----------
        impute_columns : list of str
            Columns to clean and impute.
        
        Returns:
        --------
        pd.DataFrame or None
            DataFrame with outliers replaced and missing values imputed.
        """
        df = self.df
        if df is None:
            print("!!! ERROR: No data loaded.")
            return None
        
        df = df.copy()
        
        # Replace outliers with median
        if 'Outliers_Flag' in df.columns and df['Outliers_Flag'].any():
            outlier_mask = df['Outliers_Flag']
            print("🔹 Replacing outliers with median for the following columns:")
            print(f"   {impute_columns}")
            for col in impute_columns:
                if col in df.columns:
                    median_val = df.loc[~outlier_mask, col].median(skipna=True)
                    df.loc[outlier_mask, col] = median_val

        # Impute remaining missing values with median
        print("🔹 Imputing remaining missing values with median for key columns.")
        for col in impute_columns:
            if col in df.columns:
                median_val = df[col].median(skipna=True)
                df[col].fillna(median_val, inplace=True)

        print("✅ Outliers replaced and missing values imputed.")
        self.df = df
        return df

    def save_cleaned_data(self, output_path):
        """
        Save the cleaned DataFrame to a CSV file. Drops 'Outliers_Flag' before saving.

        Parameters:
        -----------
        output_path : str
            Path where the cleaned CSV will be saved.
        """
        df = self.df
        if df is None:
            print("!!! ERROR: No data loaded.")
            return
        
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        try:
            if 'Outliers_Flag' in df.columns:
                df = df.drop(columns=['Outliers_Flag'])
                
            df.to_csv(output_path, index=False)
            print(f"\n✅ Cleaned Data Saved successfully to: {output_path}")
        except Exception as e:
            print(f"!!! ERROR: Could not save file. {e}")
