import requests
from google.auth import default
from google.auth.transport.requests import Request
import sys
import os
import json
import timeit 


# Add the main directory to the system path
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
main_dir = os.path.dirname(script_dir)
sys.path.append(main_dir)

# Import the function from main.py
from main import run

# generate sample json for local testing
##  specify number of calls to generate 
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

## Write the modified object to a new file
with open('example_requests.json', 'w') as f:
    json.dump(obj, f)

# load sample json data 
with open('example_requests.json', 'r') as f:
    request = json.load(f)

## run test with simple timer 
start_time = timeit.default_timer()
run(request, local = True)
end_time = timeit.default_timer()
execution_time = end_time - start_time
print(f"Executed the function in {execution_time} seconds")


## delete sample file 
os.remove('example_requests.json')
