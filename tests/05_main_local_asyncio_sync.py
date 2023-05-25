# Use asyncio to make a synrchronous request locally (not in CF) to replacate
# synchronous script with requests for understanding
import asyncio
import aiohttp 
import json
from google.auth import default
from google.auth.transport.requests import Request

projectId = "demos-vertex-ai"
datasetId = "z_test"
tableId = "crm_account"
url = f"https://bigquery.googleapis.com/bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}/rowAccessPolicies"

async def main():
    # Use the default credentials to obtain an access token
    creds, _ = default(scopes=["https://www.googleapis.com/auth/bigquery"])
    creds.refresh(Request())

    # Set the authorization header using the access token
    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            print(resp.status)
            print(await resp.json())

if __name__ == "__main__":
    # load sample json data
    with open('example_requests.json', 'r') as f:
        request = json.load(f)
        # print(request)
    asyncio.run(main())
