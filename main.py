import json
import requests
from google.auth import default
from google.auth.transport.requests import Request
import time


def get_row_access_polices(request, local = False):
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
    
    for i, call in enumerate(calls, 1):
        print(f"API call #: {i}")
        # set tableId as variable for passing into rowAccessPolicies API call
        projectId, datasetId, tableId = call[0], call[1], call[2]

        # Set the URL for the BigQuery API endpoint
        url = f"https://bigquery.googleapis.com/bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}/rowAccessPolicies"

        # Send the query using the requests module
        response = requests.get(url, headers=headers)

        # append results to replies (output)
        replies.append(response.json())

    return json.dumps({
        'replies': [json.dumps(reply) for reply in replies]
    })