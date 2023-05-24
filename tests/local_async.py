import asyncio
from aiohttp import ClientSession
from google.auth.transport.requests import Request
from google.auth import default
from typing import List
import json


async def get_row_access_polices(request,
                                 local=False):
    if local:
        request_json = request
    else:
        request_json = request.get_json(silent=True)
    replies = []
    calls = request_json['calls']

    async def fetch(session, url, headers, i):
        print(f"API call #: {i}")
        async with session.get(url, headers=headers) as response:
            reply = await response.json()
            if local:
                print(reply)
            return reply

    async def bound_fetch(sem, session, url, headers, i):
        # Getter function with semaphore.
        async with sem:
            return await fetch(session, url, headers, i)

    # Restricting to 90 requests per second
    sem = asyncio.Semaphore(90)

    async with ClientSession() as session:
        tasks = []
        for i, call in enumerate(calls, 1):
            # set tableId as variable for passing into rowAccessPolicies API call
            projectId = call[0]
            datasetId = call[1]
            tableId = call[2]

            # Set the URL for the BigQuery API endpoint
            url = f"https://bigquery.googleapis.com/bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}/rowAccessPolicies"

            # Use the default credentials to obtain an access token
            creds, _ = default(
                scopes=["https://www.googleapis.com/auth/bigquery"])
            creds.refresh(Request())

            # Set the authorization header using the access token
            headers = {
                "Authorization": f"Bearer {creds.token}",
                "Content-Type": "application/json"
            }

            # Add tasks to the task list
            task = asyncio.ensure_future(
                bound_fetch(sem, session, url, headers, i))
            tasks.append(task)

        # Collect all responses as they come in
        responses = await asyncio.gather(*tasks)

    # append results to replies (output)
    replies.extend(responses)

    return json.dumps({
        'replies': [json.dumps(reply) for reply in replies]
    })


# load sample json data
with open('example_requests.json', 'r') as f:
    request = json.load(f)

# print(request)
# Use myfunction as needed
get_row_access_polices(request, local=True)
