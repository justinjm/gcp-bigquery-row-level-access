import json
import aiohttp
from google.auth import default
from google.auth.transport.aiohttp_req import AiohttpClient
import asyncio


async def get_row_access_policies(request):
    # request_json = request.get_json(silent=True) # CLOUD FUNCTION
    request_json = request  # LOCAL TESTING
    replies = []
    calls = request_json['calls']
    sem = asyncio.Semaphore(90)

    async def fetch(call, session):
        async with sem:
            projectId = call[0]
            datasetId = call[1]
            tableId = call[2]
            url = f"https://bigquery.googleapis.com/bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}/rowAccessPolicies"

            creds, _ = default(
                scopes=["https://www.googleapis.com/auth/bigquery"])
            creds.refresh(AiohttpClient())

            headers = {
                "Authorization": f"Bearer {creds.token}",
                "Content-Type": "application/json"
            }

            async with session.get(url, headers=headers) as response:
                replies.append(await response.json())

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, call in enumerate(calls, 1):
            print(f"API call #: {i}")
            tasks.append(asyncio.create_task(fetch(call, session)))

        await asyncio.gather(*tasks)

    return json.dumps({
        'replies': [json.dumps(reply) for reply in replies]
    })
