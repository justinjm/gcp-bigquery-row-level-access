import requests
from google.auth import default
from google.auth.transport.requests import Request
import sys
import os
import json


# Add the main directory to the system path
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
main_dir = os.path.dirname(script_dir)
sys.path.append(main_dir)

# Import the function from main.py
from main2 import run

# load sample json data 
with open('example_requests.json', 'r') as f:
    request = json.load(f)

# Use myfunction as needed
run(request, local = True)
