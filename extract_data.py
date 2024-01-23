import pandas as pd
from typing import List
import os

def get_data_from_database(show_files_head=False):
    """
    Retrieves travel-related data from an Excel file and organizes it into separate lists for easier analysis.

    Returns:
        List[str]: data_info_headers - List of column headers as strings, representing city information [ID_header, header1, header2, etc].
        List[List[int]]: data_info - Nested list of values, each sublist contains details for a specific city [ID, data_country, data_city, etc]. 
        List[str]: data_headers - List of column headers as strings, representing various travel metrics [ID_header, header1, header2, header3, etc].
        List[List[int]]: travel_metrics - Nested list of values, each sublist contains the metrics for a specific city [ID, data_safety, data_comfort, data, etc]. 
    """

    # Get the current working directory to construct the file path
    current_working_directory = os.getcwd()

    # Define the file name. Change this to actual file name
    file_name = "example_base.xlsx"

    # Construct the full file path
    file_path = os.path.join(current_working_directory, file_name)

    # Check if the file exists before attempting to read it
    if os.path.isfile(file_path):
        # Load the Excel file into a pandas DataFrame for the "data" sheet
        df_data = pd.read_excel(file_path, sheet_name="data")

        # Load the Excel file into a pandas DataFrame for the "data_info" sheet
        # an easy way to check whether data is well-structured
        df_data_info = pd.read_excel(file_path, sheet_name="data_info")

        # Optionally, print the first few rows of both DataFrames to check the data
        if show_files_head:
            print("Data sheet:")
            print(df_data.head())

            print("Data_info sheet:")
            print(df_data_info.head())
    else:
        # If the file is not found, print an error message
        print(f"File does not exist: {file_path}")
        return

    # Extract column headers from the DataFrames and data
    data_info_headers = df_data_info.columns.tolist()
    data_info: List[List[any]] = df_data_info.iloc[:,:].values.tolist()

    data_headers = df_data.columns.tolist()
    data: List[List[int]] = df_data.iloc[:, :].values.tolist()

    # Return the organized data
    return data_info_headers, data_info, data_headers, data

# Main function execution
if __name__ == "__main__":
    retu = get_data_from_database()
    print(retu)
