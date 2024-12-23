import asyncio
import base64
import csv
import os
from pyinjective.async_client import AsyncClient
from pyinjective.core.network import Network

async def get_token_status(token_id: str, address: str, client: AsyncClient) -> str:
    """Query the contract to check if the token is burned."""
    query_data = f'{{"owner_of": {{"token_id": "{token_id}"}}}}'  # Query for ownership

    try:
        contract_state = await client.fetch_smart_contract_state(address=address, query_data=query_data)
        decoded_data = base64.b64decode(contract_state['data']).decode('utf-8')

        if decoded_data == "null" or decoded_data == "":  # No owner found, maybe burned
            return "Burned"
        else:
            return "Active"

    except Exception as e:
        print(f"Error fetching status for token {token_id}: {e}")
        return "Error"

async def process_csv(input_path: str, output_path: str, contract_address: str) -> None:
    """Process the CSV file, add token status, and write to a new CSV."""
    # Initialize the client
    network = Network.mainnet()  # Use mainnet or testnet as appropriate
    client = AsyncClient(network)
    
    # Read the input CSV
    with open(input_path, mode='r') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)

    # Add a new 'status' column and query each token_id
    for row in rows:
        token_id = row['token_id']
        status = await get_token_status(token_id, contract_address, client)
        row['status'] = status

    # Write the updated CSV with the new status column
    fieldnames = reader.fieldnames + ['status']
    with open(output_path, mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# Main entry point
if __name__ == "__main__":
    input_file_path = 'input/nft_data.csv'  # Replace with your input file path
    output_file_path = 'output/checked-for-burnt.csv'  # Replace with your output file path
    contract_address = 'inj1nlf4avwqdgnn499a5u7m9qdpj0f5l275k6c99y'  # Replace with your contract address
    
    # Run the processing
    asyncio.run(process_csv(input_file_path, output_file_path, contract_address))
