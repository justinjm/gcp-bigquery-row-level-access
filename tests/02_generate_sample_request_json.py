import json

obj = {
    "requestId": "124ab1c",
    "caller": "//bigquery.googleapis.com/projects/myproject/jobs/myproject:US.bquxjob_5b4c112c_17961fafeaf",
    "sessionUser": "test-user@test-company.com",
    "userDefinedContext": {
        "key1": "value1",
        "key2": "v2"
    },
    "calls": [
        ["demos-vertex-ai", "z_test", "crm_account"],
        ["demos-vertex-ai", "z_test", "crm_account"]
    ]
}

for _ in range(10000):
    obj["calls"].append(["demos-vertex-ai", "z_test", "crm_account"])

# Write the modified object to a new file
with open('example_requests.json', 'w') as f:
    json.dump(obj, f)

