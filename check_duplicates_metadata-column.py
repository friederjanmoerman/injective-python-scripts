import pandas as pd
import os

# ANSI escape codes for coloring
GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"

# Input folder containing CSV files
input_folder = 'input'

# Iterate through files in the input folder
for file_name in os.listdir(input_folder):
    if file_name.endswith('.csv'):
        file_path = os.path.join(input_folder, file_name)

        try:
            # Read the input CSV file
            df = pd.read_csv(file_path, sep=';')

            # Strip whitespace from all column names
            df.columns = df.columns.str.strip()

            # Check if the 'metadata_uri' column exists in the DataFrame
            if 'metadata_uri' not in df.columns:
                print(f"{RED}Column 'metadata_uri' not found in the file: {file_name}{RESET}")
                continue

            # Find duplicates in the 'metadata_uri' column
            duplicates = df['metadata_uri'].value_counts()
            duplicate_count = duplicates[duplicates > 1]

            if not duplicate_count.empty:
                print(f"\n{GREEN}File: {file_name}{RESET}")
                print(f"Duplicate counts in 'metadata_uri' column:\n{duplicate_count}\n")
            else:
                print(f"\n{GREEN}File: {file_name}{RESET}")
                print("No duplicates found in 'metadata_uri' column.\n")

        except Exception as e:
            print(f"{RED}Error processing file {file_name}: {e}{RESET}")
