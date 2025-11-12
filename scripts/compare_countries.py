import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

# Set a consistent style for all plots
sns.set_style("whitegrid")

class ComparisonHandler:
    """
    Handles the loading, combining, analysis, and visualization for 
    cross-country solar potential comparison.
    
    The file paths are passed dynamically during initialization.
    """
    
    def __init__(self, file_paths: dict):
        """
        Initialize country paths and constants.

        Parameters:
        -----------
        file_paths : dict
            A dictionary where keys are country names (str) and values are 
            the absolute or relative paths (str) to their clean CSV files.
        """
        if not isinstance(file_paths, dict) or not file_paths:
            raise ValueError("file_paths must be a non-empty dictionary mapping country names to file paths.")
        
        # Store file paths and extract country names dynamically
        self.FILE_PATHS = file_paths
        self.COUNTRIES = list(file_paths.keys())
        
        # Constants for solar metrics
        # GHI (Global Horizontal Irradiance), DNI (Direct Normal Irradiance), DHI (Diffuse Horizontal Irradiance)
        self.METRICS = ['GHI', 'DNI', 'DHI']
        
        self.df_combined = None
        self.summary_table = None

    def load_and_combine_data(self):
        """Load cleaned data from each country and combine into a single DataFrame."""
        all_data = []
        print("Loading cleaned datasets for cross-country comparison...")

        # Iterate over the dynamic FILE_PATHS dictionary
        for country, path in self.FILE_PATHS.items():
            try:
                # Load the CSV
                df = pd.read_csv(path)
                
                # Add a 'Country' column for comparison
                df['Country'] = country
                all_data.append(df)
                print(f"✅ Loaded {country} with {len(df)} rows.")
            except FileNotFoundError:
                print(f"!!! ERROR: File not found for {country} at {path}. Skipping this country.")
            except Exception as e:
                print(f"!!! ERROR: Could not load data for {country}. {e}")
        
        # Concatenate all DataFrames
        self.df_combined = pd.concat(all_data, ignore_index=True)
        
        if self.df_combined.empty:
            print("\n!!! All datasets failed to load or were empty. Cannot proceed with comparison.")
            return False
        else:
            print(f"\nTotal combined rows: {len(self.df_combined)}")
            print("-" * 50)
            print("Combined Data Head:")
            print(self.df_combined.head())
            return True

    def generate_boxplots(self):
        """Generate boxplots for GHI, DNI, and DHI across countries."""
        if self.df_combined is None or self.df_combined.empty:
            print("Cannot generate boxplots: Combined data is not loaded or is empty.")
            return

        print("\n--- Generating Boxplots for GHI, DNI, and DHI comparison ---")
        
        metrics_to_plot = [m for m in self.METRICS if m in self.df_combined.columns]
        
        if not metrics_to_plot:
            print("Skipping plots: No solar irradiance metrics (GHI, DNI, DHI) found in combined data.")
            return
            
        fig, axes = plt.subplots(nrows=1, ncols=len(metrics_to_plot), figsize=(5 * len(metrics_to_plot), 6))
        
        # Handle case for a single plot
        if len(metrics_to_plot) == 1:
            axes = [axes] 

        for ax, metric in zip(axes, metrics_to_plot):
            # NO FILTERING: Assuming data is already cleaned for non-positive values
            
            sns.boxplot(
                x='Country', 
                y=metric, 
                data=self.df_combined, # Removed .copy() and the filter
                palette='viridis', 
                hue='Country', 
                ax=ax, 
                legend=False
            )
            # Updated title to reflect that it's the distribution on the cleaned (daytime/positive) data
            ax.set_title(f'Distribution of {metric}', fontsize=12) 
            ax.set_ylabel(rf'{metric} ($\mathrm{{W/m^2}}$)')
            ax.set_xlabel('')
            
        plt.tight_layout()
        plt.show()

    def generate_summary_table(self):
        """Calculate and display mean, median, and std deviation for key metrics."""
        if self.df_combined is None or self.df_combined.empty:
            print("Cannot generate summary table: Combined data is not loaded or is empty.")
            return
            
        print("\n--- Generating Summary Table for GHI, DNI, and DHI ---")
        
        df_data = self.df_combined
        metrics_for_summary = [m for m in self.METRICS if m in self.df_combined.columns]


        if not metrics_for_summary:
            print("Skipping summary: No relevant solar irradiance metrics found.")
            return
            
        summary_table = (
            df_data
            .groupby('Country')[metrics_for_summary]
            .agg(['mean', 'median', 'std'])
        )
        
        self.summary_table = summary_table.round(2) 
        
        print(self.summary_table)
        return self.summary_table

    def run_statistical_tests(self):
        """Run ANOVA and Kruskal–Wallis tests on GHI to assess significance of differences."""
        if self.df_combined is None or self.df_combined.empty:
            print("Cannot run statistical tests: Combined data is not loaded or is empty.")
            return
        
        if 'GHI' not in self.df_combined.columns:
            print("Skipping tests: 'GHI' column not available.")
            return
            
        print("\n--- Running Statistical Tests on GHI across countries ---")
        
        df_test_data = self.df_combined
            
        # Prepare data grouped by country, dropping NaNs
        groups = [group["GHI"].dropna().values for _, group in df_test_data.groupby("Country")]
        
        # Remove empty groups if a country had no GHI data
        groups = [g for g in groups if g.size > 0] 
        
        if len(groups) < 2:
            print("Skipping tests: Need data from at least two countries.")
            return

        # --- One-way ANOVA ---
        anova_stat, anova_p = stats.f_oneway(*groups)

        # --- Kruskal–Wallis test (non-parametric alternative) ---
        krustal_stat, krustal_p = stats.kruskal(*groups) # Corrected typo in variable name in original code

        # --- Display results ---
        print("\n--- Statistical Testing Results ---")
        print(f"One-way ANOVA: F-statistic = {anova_stat:.3f}, p-value = {anova_p:.5f}")
        print(f"Kruskal–Wallis: H-statistic = {krustal_stat:.3f}, p-value = {krustal_p:.5f}")

        # --- Interpretation hint ---
        if anova_p < 0.05 or krustal_p < 0.05:
            print("\n→ The differences in GHI between countries are statistically **significant** (p < 0.05).")
        else:
            print("\n→ No statistically significant differences found in GHI between countries (p ≥ 0.05).")


    def plot_average_ghi_bar_chart(self):
        """Plot a bar chart of countries ranked by their average GHI."""
        if self.df_combined is None or self.df_combined.empty:
            print("Cannot plot bar chart: Combined data is not loaded or is empty.")
            return

        if 'GHI' not in self.df_combined.columns:
            print("Skipping bar chart: 'GHI' column not available.")
            return

        print("\n--- Plotting Average GHI by Country ---")
        
        # Compute average GHI per country
        ghi_avg = self.df_combined.groupby("Country")["GHI"].mean().sort_values(ascending=False)

        # Plot
        plt.figure(figsize=(6, 4))
        sns.barplot(
            x=ghi_avg.index,
            y=ghi_avg.values,
            hue=ghi_avg.index,
            palette="viridis",
            legend=False
        )

        plt.title("Average GHI by Country", fontsize=14)
        plt.ylabel(r'Average GHI ($\mathrm{W/m^2}$)', fontsize=10)
        plt.xlabel('Country', fontsize=10)
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.show()

    def run_comparison(self):
        """Execute the full cross-country comparison workflow."""
        print("🌍 Starting Cross-Country Solar Potential Comparison Workflow...")
        
        # Step 1: Load and combine data
        if self.load_and_combine_data():
            
            # Step 2: Boxplots
            self.generate_boxplots()
            
            # Step 3: Summary Table
            self.generate_summary_table()
            
            # Step 4: Statistical Tests
            self.run_statistical_tests()
            
            # Step 5: Average GHI Bar Chart
            self.plot_average_ghi_bar_chart()
            
            print("\n✅ Cross-Country Comparison workflow completed.")

if __name__ == '__main__':
    # Define file paths dynamically outside the class logic
    # NOTE: The relative paths below require a specific directory structure 
    # to be run successfully outside of the context they were created in.
    DYNAMIC_FILE_PATHS = {
        'Benin': '../../data/benin/benin_clean.csv',
        'Sierra Leone': '../../data/sierra-leone/sierra_leone_clean.csv',
        'Togo': '../../data/togo/togo_clean.csv'
        # To add a new country (e.g., Ghana), simply add an entry here:
        # 'Ghana': '../../data/ghana/ghana_clean.csv'
    }

    # Execute the comparison workflow when the script is run directly
    try:
        handler = ComparisonHandler(file_paths=DYNAMIC_FILE_PATHS)
        handler.run_comparison()
    except ValueError as e:
        print(f"Workflow failed to start: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during the workflow: {e}")