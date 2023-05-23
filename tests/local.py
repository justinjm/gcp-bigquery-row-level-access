import requests
from google.auth import default
from google.auth.transport.requests import Request
import time

projectId = "demos-vertex-ai"
datasetId = "z_test"
tableId = "crm_account"

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
response = requests.get(url, headers=headers)

print(response.json())

# # append results to replies (output)
# replies.append(response.json())

# return json.dumps({
# 'replies': [json.dumps(reply) for reply in replies]