import pandas as pd
from typing import List
import os

def get_data_from_database():
    """
    Retrieves travel-related data from an Excel file and organizes it into separate lists for easier analysis.

    Returns:
        List[str]: city_option_headers - List of column headers as strings, representing city information (e.g., city, country).
        List[List[int]]: city_options - Nested list of values, each sublist contains details for a specific city. 
        List[str]: travel_metric_headers - List of column headers as strings, representing various travel metrics (e.g., cost, comfort, safety).
        List[List[int]]: travel_metrics - Nested list of values, each sublist contains the metrics for a specific city. 
    """

    # Get the current working directory to construct the file path
    current_working_directory = os.getcwd()

    # Define the file name. Change this to your actual file name
    file_name = "example_base.xlsx"

    # Construct the full file path
    file_path = os.path.join(current_working_directory, file_name)

    # Check if the file exists before attempting to read it
    if os.path.isfile(file_path):
        # Load the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path)
        # Optionally, print the first few rows to check the data
        # print(df.head())
    else:
        # If the file is not found, print an error message
        print(f"File does not exist: {file_path}")
        return

    # Define the index where city data ends and travel metric data begins
    city_data_start_index = 2

    # Extract column headers from the DataFrame
    column_headers = df.columns.tolist()

    # Split the headers into city information headers and travel metric headers
    city_option_headers: List[str] = column_headers[:city_data_start_index]
    travel_metric_headers: List[str] = column_headers[city_data_start_index:]

    # Split the DataFrame into two parts: city information and travel metrics
    city_options: List[List[str]] = df.iloc[:, :city_data_start_index].values.tolist()
    travel_metrics: List[List[int]] = df.iloc[:, city_data_start_index:].values.tolist()

    # Return the organized data
    return city_option_headers, city_options, travel_metric_headers, travel_metrics

# Main function execution
if __name__ == "__main__":
    retu = get_data_from_database()
    print(retu)
