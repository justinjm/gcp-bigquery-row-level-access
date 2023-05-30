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

# load sample json data 
with open('example_requests.json', 'r') as f:
    request = json.load(f)

## run test with simple timer 
start_time = timeit.default_timer()
run(request, local = True)
end_time = timeit.default_timer()
execution_time = end_time - start_time
print(f"Executed the function in {execution_time} seconds")