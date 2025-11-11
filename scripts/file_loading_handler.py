
import pandas as pd

class FileLoadingHandler:
    """
    A base class providing common functionality for data handling,
    like initializing with a file path and a reusable data loading method.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        
    def load_data(self):
        """
        Load the dataset from the CSV file and convert 'Timestamp' to datetime if present.
        
        This method is reused by both DatasetHandler and EDAHandler.

        Returns:
        --------
        pd.DataFrame or None
            Loaded DataFrame or None if loading failed.
        """
        try:
            self.df = pd.read_csv(self.file_path)
            
            # Convert 'Timestamp' to datetime objects
            if 'Timestamp' in self.df.columns:
                self.df['Timestamp'] = pd.to_datetime(self.df['Timestamp'])
                print("✅ 'Timestamp' column successfully converted to datetime objects.")
            
            return self.df
        except FileNotFoundError:
            print(f"!!! ERROR: The file '{self.file_path}' was not found.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during loading: {e}")
            return None