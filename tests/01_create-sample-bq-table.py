import pandas as pd
from google.cloud import bigquery


# Create a DataFrame with 3 columns of string values to mimic
# the INFORMATION_SCHEMA dataset:
data = {'table_catalog': ['demos-vertex-ai'] * 10000,
        'table_schema': ['z_test'] * 10000, 
        'table_name': ['crm_account'] * 10000}

df = pd.DataFrame(data)

# Initialize a BigQuery client
# Make sure your GOOGLE_APPLICATION_CREDENTIALS environment variable 
# is set correctly
client = bigquery.Client()

# Specify your BigQuery dataset and table
dataset_id = 'z_test' # Update dataset_id if you'd like
table_id = 'z_sample_info_schema_input'  # Update dataset ID if you'd like

# Check if the dataset exists and create it if it doesn't
dataset_ref = client.dataset(dataset_id)
try:
    # Will raise NotFound if dataset does not exist.
    client.get_dataset(dataset_ref)
    print(f"Dataset {dataset_id} already exists.")
except Exception as e:
    print(f"Dataset {dataset_id} does not exist. Creating now...")
    # create new BigQuery dataset
    client.create_dataset(dataset_ref)  
    print(f"Dataset {dataset_id} created.")

# Check if the table exists already
try:
    client.get_table(f'{dataset_id}.{table_id}')
except Exception as e:
    print(
        f'Table {dataset_id}.{table_id} does not exist. Creating now...')
    # Create a new BigQuery table 
    table_ref = client.dataset(dataset_id).table(table_id)
else:
    raise RuntimeError(f'Table {table_id} already exists.')

# upload the DataFrame 
job = client.load_table_from_dataframe(df, table_ref)

# Wait for the job to complete
job.result()

print("Uploaded {} rows to {}:{}.".format(
    job.output_rows, dataset_id, table_id))


# pip3 install pyarrow 