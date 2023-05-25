import json

with open('example_requests.json', 'r') as f:
    obj = json.load(f)

print(obj)
