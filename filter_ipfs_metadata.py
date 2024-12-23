import pandas as pd
import os
import json

# ANSI escape codes for coloring
GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"

# Input, metadata, and output folder paths
input_folder = 'input'
metadata_folder = 'ipfs'
output_folder = 'output'

# Tag to search for in metadata
tag_to_search = 'christmas'

# Function to check for tags and retrieve edition
def contains_tags_and_edition(metadata_path):
    try:
        if not os.path.exists(metadata_path):
            print(f"{RED}Metadata file not found: {metadata_path}{RESET}")
            return False, None

        with open(metadata_path, 'r') as file:
            metadata = json.load(file)

        metadata_str = json.dumps(metadata).lower()

        if tag_to_search in metadata_str:
            # Retrieve the edition value if it exists
            edition = metadata.get('edition', None)
            return True, edition
        else:
            print(f"{RED}Tag not found in metadata: {metadata_path}{RESET}")
            return False, None

    except Exception as e:
        print(f"{RED}Error processing metadata file {metadata_path}: {e}{RESET}")
        return False, None

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
                print(f"Column 'metadata_uri' not found in the file: {file_name}")
                continue

            # Prepare to collect rows with additional edition data
            filtered_rows = []
            for index, uri in df['metadata_uri'].items():
                if 'ipfs://' in uri:
                    # Construct the local metadata file path
                    ipfs_hash = uri.replace('ipfs://', '').split('/')[0]
                    metadata_file = uri.split('/')[-1]  # Extract the JSON file name

                    # Check for metadata folder structure
                    metadata_path = os.path.join(metadata_folder, ipfs_hash, "metadata", metadata_file)
                    if not os.path.exists(metadata_path):
                        # Fallback to direct file within hash folder
                        metadata_path = os.path.join(metadata_folder, ipfs_hash, metadata_file)

                    # Check for tag and retrieve edition
                    has_tag, edition = contains_tags_and_edition(metadata_path)
                    if has_tag:
                        row = df.iloc[index].copy()
                        row['edition'] = edition  # Add the edition column
                        filtered_rows.append(row)

            # Create a filtered DataFrame
            filtered_df = pd.DataFrame(filtered_rows)

            # Ensure the output folder exists
            os.makedirs(output_folder, exist_ok=True)

            # Save the filtered DataFrame to a CSV file
            output_file = os.path.join(output_folder, f"filtered_{file_name}")
            filtered_df.to_csv(output_file, index=False)

            print(f"Filtered dataset from {file_name} has been saved to: {output_file}")

        except Exception as e:
            print(f"Error processing file {file_name}: {e}")
