import asyncio
import json
import requests
from google.auth import default
from google.auth.transport.requests import Request
import time


async def get_row_access_policies(request):
    # request_json = request.get_json(silent=True) # CLOUD FUNCTION
    request_json = request # LOCAL TESTING
    replies = []
    calls = request_json['calls']
    for i, call in enumerate(calls, 1):
        print(f"API call #: {i}")
        # set tableId as variable for passing into rowAccessPolicies API call
        projectId = call[0]
        datasetId = call[1]
        tableId = call[2]

        # Set the URL for the BigQuery API endpoint
        url = f"https://bigquery.googleapis.com/bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}/rowAccessPolicies"

        # Use the default credentials to obtain an access token
        creds, _ = default(scopes=["https://www.googleapis.com/auth/bigquery"])
        creds.refresh(Request())

        # Set the authorization header using the access token
        headers = {
            "Authorization": f"Bearer {creds.token}",
            "Content-Type": "application/json"
        }

        # Send the query using the requests module
        response = await requests.get(url, headers=headers)

        if local:
            print(response.json())

        # append results to replies (output)
        replies.append(response.json())

    return json.dumps({
        'replies': [json.dumps(reply) for reply in replies]
    })


async def main():
    # Create a semaphore to throttle the requests
    sem = asyncio.Semaphore(90)

    # Create a task for each API call
    tasks = []
    for call in calls:
        tasks.append(asyncio.create_task(
            get_row_access_policies(call), sem=sem))

    # Wait for all tasks to complete
    await asyncio.wait(tasks)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
