# Use asyncio to make a synrchronous request locally (not in CF) to replacate
# synchronous script with requests for understanding
import asyncio
import aiohttp 
import json
from google.auth import default
from google.auth.transport.requests import Request

async def get_row_access_polices(request):
    # Use the default credentials to obtain an access token
    creds, _ = default(scopes=["https://www.googleapis.com/auth/bigquery"])
    creds.refresh(Request())

    # Set the authorization header using the access token
    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json"
    }

    # request_json = request.get_json(silent=True) # prod
    request_json = request # test - local
    replies = []
    calls = request_json['calls']
    
    async with aiohttp.ClientSession() as session:
        for i, call in enumerate(calls, 1):
            print(f"API call #: {i}")
            # set tableId as variable for passing into rowAccessPolicies API call
            projectId, datasetId, tableId = call[0], call[1], call[2]
            # set url  
            url = f"https://bigquery.googleapis.com/bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}/rowAccessPolicies"
        
            async with session.get(url, headers=headers) as response:
                replies.append(await response.json())

        # print(replies)   # print for debugging
        return json.dumps({
            'replies': [json.dumps(reply) for reply in replies]
        })    

def run(request):
    asyncio.run(get_row_access_polices(request = request))    


# load sample json data
# with open('example_requests.json', 'r') as f:
#     request = json.load(f)
#     # print(request) # print for debugging
#     # time.sleep(0.01) # add sleep of 10ms here if needed 
# asyncio.run(get_row_access_polices(request = request))

    
    
