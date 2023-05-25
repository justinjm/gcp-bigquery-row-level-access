import asyncio
from aiohttp import ClientSession
import json
from google.auth import default
from google.auth.transport.requests import Request


async def hello(url: str, queue: asyncio.Queue):       
    # Use the default credentials to obtain an access token
    creds, _ = default(scopes=["https://www.googleapis.com/auth/bigquery"])
    creds.refresh(Request())

    # Set the authorization header using the access token
    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json"
    }

    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            result = {"response": await response.text(), "url": url}
            await queue.put(result)

async def main():
    projectId = "demos-vertex-ai"
    datasetId = "z_test"
    tableId = "crm_account"
    url = f"https://bigquery.googleapis.com/bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}/rowAccessPolicies"
    results = []
    queue = asyncio.Queue()
    async with asyncio.TaskGroup() as group:
        for i in range(10):
            group.create_task(hello(url.format(i), queue))

    while not queue.empty():
        results.append(await queue.get())
    
    print(json.dumps(results))


asyncio.run(main()) 


# if __name__ == "__main__":
#     # load sample json data
#     with open('example_requests.json', 'r') as f:
#         request = json.load(f)

#     asyncio.run(main()) 

## TODO
# * add throttling/limitting of 90 requests per second (100 max)
# * add batch input to mimic BQ remote function behavior
# * prepare code for CF / testing in GCP