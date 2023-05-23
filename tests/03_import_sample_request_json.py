import json

with open('example_requests.json', 'r') as f:
    obj = json.load(f)

print(obj)

# request_json = obj.get_json(silent=True)
# calls = request_json['calls']

# calls = obj['calls']
# print(calls)

# for call in calls:
#     # set tableId as variable for passing into rowAccessPolicies API call
#     projectId = call[0]
#     print(projectId)
