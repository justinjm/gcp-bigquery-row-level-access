import asyncio
from aiohttp import ClientSession
import json
from google.auth import default
from google.auth.transport.requests import Request


async def get_row_access_polices(url: str, queue: asyncio.Queue):       
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

async def main(request):
    # request_json = request.get_json(silent=True) # prod
    request_json = request # test - local
    calls = request_json['calls']
    results = []
    queue = asyncio.Queue()
    async with asyncio.TaskGroup() as group:
        for call in calls:
            projectId, datasetId, tableId = call[0], call[1], call[2]
            url = f"https://bigquery.googleapis.com/bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}/rowAccessPolicies"
            group.create_task(get_row_access_polices(url, queue))

    while not queue.empty():
        results.append(await queue.get())
    
    print(json.dumps(results))


if __name__ == "__main__":
    # load sample json data
    with open('example_requests.json', 'r') as f:
        request = json.load(f)
    asyncio.run(main(request = request)) 

## TODO
# * add throttling/limitting of 90 requests per second (100 max)
# * add batch input to mimic BQ remote function behavior
# * prepare code for CF / testing in GCP
## * input = object = request json (`for call in calls`)
## * output = object "replies"  
## * CF entrypoint ?? 
## * CF requirements.txt

