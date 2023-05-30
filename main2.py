import json
import time
from google.auth import default
from google.auth.transport.requests import Request
import asyncio
import aiohttp 


async def get_row_access_polices(request, local=False):
    # Use the default credentials to obtain an access token
    creds, _ = default(scopes=["https://www.googleapis.com/auth/bigquery"])
    creds.refresh(Request())

    # Set the authorization header using the access token
    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json"
    }
    
    if local:
        request_json = request
    else: 
        request_json = request.get_json(silent=True)
        
    replies = []
    calls = request_json['calls']
    
    async with aiohttp.ClientSession() as session:
        for i, call in enumerate(calls, 1):
            # 10ms sleep to stay under 100 requests per user per second API quota
            time.sleep(0.01) 

            print(f"API call #: {i}")
            projectId, datasetId, tableId = call[0], call[1], call[2]
            url = f"https://bigquery.googleapis.com/bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}/rowAccessPolicies"
        
            async with session.get(url, headers=headers) as response:
                replies.append(await response.json())

        return json.dumps({
            'replies': [json.dumps(reply) for reply in replies]
        })    

def run(request, local=False):
    asyncio.run(get_row_access_polices(request = request,
                                       local = local))    

