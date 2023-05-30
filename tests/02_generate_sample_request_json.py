import json

# number of calls to generate 
n = 10

obj = {
    "requestId": "124ab1c",
    "caller": "//bigquery.googleapis.com/projects/myproject/jobs/myproject:US.bquxjob_5b4c112c_17961fafeaf",
    "sessionUser": "test-user@test-company.com",
    "userDefinedContext": {
        "key1": "value1",
        "key2": "v2"
    },
    "calls": [
        ["demos-vertex-ai", "z_test", "crm_account"]
    ]
}

## generate calls objects, minus 1  since we want a round number and have 
## one set above for example 
for _ in range(n-1):
    obj["calls"].append(["demos-vertex-ai", "z_test", "crm_account"])

# Write the modified object to a new file
with open('example_requests.json', 'w') as f:
    json.dump(obj, f)