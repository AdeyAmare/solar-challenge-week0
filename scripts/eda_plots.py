import pandas as pd
import numpy as np 

import matplotlib.pyplot as plt
import seaborn as sns

from windrose import WindroseAxes

sns.set_style("whitegrid")

from file_loading_handler import FileLoadingHandler


class EDAHandler(FileLoadingHandler):
    """
    Class to perform Exploratory Data Analysis (EDA) on a dataset,
    including time series plots, cleaning impact analysis, correlations,
    scatter/bubble plots, distribution analysis, and wind rose visualization.
    """

    def plot_time_series(self):
        """
        Plot time series for GHI, DNI, DHI, and Tamb against Timestamp.
        """
        df = self.df
        if 'Timestamp' not in df.columns:
            print("!!! ERROR: 'Timestamp' column missing.")
            return
        
        try:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        except Exception as e:
            print(f"Error converting Timestamp to datetime: {e}")
            return

        df_ts = df.set_index('Timestamp')

        # Only plot columns that exist
        cols_to_plot = [c for c in ['GHI', 'DNI', 'DHI', 'Tamb'] if c in df_ts.columns]
        if not cols_to_plot:
            print("!!! ERROR: None of GHI, DNI, DHI, Tamb are available.")
            return

        fig, axes = plt.subplots(nrows=len(cols_to_plot), ncols=1, figsize=(14, 3 * len(cols_to_plot)), sharex=True)
        if len(cols_to_plot) == 1:
            axes = [axes]
        fig.suptitle('Time Series Analysis: Raw Data', fontsize=16)

        for ax, col in zip(axes, cols_to_plot):
            df_ts[col].plot(ax=ax, linewidth=0.5)
            ax.set_title(f'{col} Over Time (Raw Data)', loc='left')
            ax.set_ylabel(col)
            ax.grid(True, linestyle='--', alpha=0.7)
        
        plt.xlabel('Date and Time')
        plt.tight_layout(rect=[0,0,1,0.98])
        plt.show()

    def plot_cleaning_impact(self):
        """
        Plot the impact of the existing solar panel cleaning flag using point plots.
        """
        df = self.df
        print("\n--- Plotting Cleaning Flag Impact (Point Plot) ---")

        required_cols = ['ModA', 'ModB', 'Cleaning']
        if not all(col in df.columns for col in required_cols):
            print("!!! ERROR: Missing one or more required columns: 'ModA', 'ModB', 'Cleaning'.")
            return

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Impact of Solar Panel Cleaning (Existing Flag)', fontsize=16)

        # Common parameters for tick labels
        xtick_labels = ['Not Cleaned', 'Cleaned']

        # --- Point plot for ModA ---
        sns.pointplot(x='Cleaning', y='ModA', data=df, 
                    hue='Cleaning', legend=False,
                    errorbar='sd', markers='o', linestyles='-', 
                    palette=['skyblue', 'orange'], ax=axes[0])
        
        axes[0].set_xticks([0, 1])
        axes[0].set_xticklabels(xtick_labels)
        axes[0].set_title('ModA')
        axes[0].set_ylabel('ModA Value')
        axes[0].set_xlabel('Cleaning Flag')

        # --- Point plot for ModB ---
        sns.pointplot(x='Cleaning', y='ModB', data=df, 
                    hue='Cleaning', legend=False,
                    errorbar='sd', markers='o', linestyles='-', 
                    palette=['skyblue', 'orange'], ax=axes[1])
        
        axes[1].set_xticks([0, 1])
        axes[1].set_xticklabels(xtick_labels)
        axes[1].set_title('ModB')
        axes[1].set_ylabel('ModB Value')
        axes[1].set_xlabel('Cleaning Flag')

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()


    def plot_correlation_heatmap(self):
        """
        Plot a correlation heatmap for available temperature and irradiance columns.
        """
        df = self.df
        print("\n--- Plotting Correlation Heatmap ---")
        corr_cols = ['GHI', 'DNI', 'DHI', 'TModA', 'TModB']
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

    def plot_scatter_relationships(self):
        """
        Plot scatter relationships for selected variable pairs (sampled for speed).
        """
        df = self.df
        print("\n--- Plotting Relationship Scatter Plots ---")
        pairs = [('WS', 'GHI'), ('WSgust', 'GHI'), ('WD', 'GHI'), ('RH', 'Tamb'), ('RH', 'GHI')]

        available_pairs = [(x, y) for x, y in pairs if x in df.columns and y in df.columns]
        if not available_pairs:
            print("!!! ERROR: No available pairs for scatter plots.")
            return

        sample_size = min(5000, len(df))
        df_sample = df.sample(n=sample_size, random_state=1)

        num_plots = len(available_pairs)
        num_cols = 2
        num_rows = (num_plots + num_cols - 1) // num_cols
        fig, axes = plt.subplots(num_rows, num_cols, figsize=(14, 6 * num_rows))
        fig.suptitle('Relationship Analysis (Sampled Data)', fontsize=16)
        axes = axes.flatten()

        for i, (x_col, y_col) in enumerate(available_pairs):
            sns.scatterplot(data=df_sample, x=x_col, y=y_col, ax=axes[i], alpha=0.6, s=10)
            axes[i].set_title(f'{y_col} vs. {x_col}')

        # Remove empty axes
        for j in range(num_plots, len(axes)):
            fig.delaxes(axes[j])
                
        plt.tight_layout(rect=[0, 0, 1, 0.97])
        plt.show()

    def plot_wind_and_distribution(self):
        """
        Plot distribution histograms for GHI and WS and generate a Wind Rose plot.
        """
        df = self.df
        print("\n--- Plotting Distribution Histograms ---")
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Histograms
        if 'GHI' in df.columns:
            sns.histplot(df['GHI'], kde=True, bins=50, ax=axes[0])
            axes[0].set_title('Distribution of GHI')
        else:
            axes[0].set_title('GHI Column Not Found')

        if 'WS' in df.columns:
            sns.histplot(df['WS'], kde=True, bins=30, ax=axes[1])
            axes[1].set_title('Distribution of Wind Speed (WS)')
        else:
            axes[1].set_title('WS Column Not Found')
            
        plt.tight_layout()
        plt.show()

        # Wind Rose
        if 'WS' in df.columns and 'WD' in df.columns:
            print("\n--- Plotting Wind Rose ---")
            try:
                plt.figure(figsize=(8, 8))
                ax = WindroseAxes.from_ax()
                wind_df = df[['WD', 'WS']].dropna()
                ax.bar(wind_df['WD'], wind_df['WS'], normed=True, opening=0.8, edgecolor='white')
                ax.set_legend(title="Wind Speed (m/s)")
                plt.title('Wind Rose (Wind Direction and Speed)')
                plt.show()
            except Exception as e:
                print(f"!!! ERROR: Could not generate Wind Rose. {e}")
        else:
            print("Skipping Wind Rose: 'WS' or 'WD' columns not found.")

    def plot_bubble_chart(self):
        """
        Plot a bubble chart of GHI vs. Tamb with bubble size proportional to RH.
        """
        df = self.df
        print("\n--- Plotting Bubble Chart (GHI vs. Tamb, Size = RH) ---")
        required_cols = ['GHI', 'Tamb', 'RH']
        if not all(col in df.columns for col in required_cols):
            print("!!! ERROR: Missing one or more required columns: 'GHI', 'Tamb', 'RH'.")
            return

        sample_size = min(5000, len(df))
        df_sample = df.sample(n=sample_size, random_state=1)
        
        plt.figure(figsize=(12, 8))
        if df_sample['RH'].max() > 0:
            size = (df_sample['RH'] / df_sample['RH'].max()) * 500
            size = size.fillna(10)
        else:
            size = 50

        scatter = plt.scatter(data=df_sample, x='Tamb', y='GHI', 
                              s=size, c='RH', 
                              cmap='viridis', alpha=0.6, 
                              edgecolors='w', linewidth=0.5)
        
        plt.xlabel('Ambient Temperature (Tamb)')
        plt.ylabel('Global Horizontal Irradiance (GHI)')
        plt.title('GHI vs. Tamb (Bubble Size = Relative Humidity, RH)')
        plt.colorbar(scatter, label='Relative Humidity (RH)')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()
