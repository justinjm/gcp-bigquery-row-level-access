import requests
from google.auth import default
from google.auth.transport.requests import Request
import time
import sys
import os
import json

# Add the main directory to the system path
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
main_dir = os.path.dirname(script_dir)
sys.path.append(main_dir)

# Import the function from main.py
from main import get_row_access_polices


# load sample json data 
request = {
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

# Use myfunction as needed
get_row_access_polices(request, local = True)






