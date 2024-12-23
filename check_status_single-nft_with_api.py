import asyncio
import base64
from pyinjective.async_client import AsyncClient
from pyinjective.core.network import Network

async def main() -> None:
    network = Network.mainnet() 
    client = AsyncClient(network)
    address = "inj1nlf4avwqdgnn499a5u7m9qdpj0f5l275k6c99y" 
    
    query_data = '{"owner_of": {"token_id": "2625"}}'

    try:
        contract_state = await client.fetch_smart_contract_state(address=address, query_data=query_data)
        
        decoded_data = base64.b64decode(contract_state['data']).decode('utf-8')
        
        print("Decoded NFT Info:", decoded_data)
    
    except Exception as e:
        print(f"Error fetching NFT info: {e}")

if __name__ == "__main__":
    asyncio.run(main())
