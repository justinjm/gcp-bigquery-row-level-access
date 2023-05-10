# Google Cloud BigQuery - Row Level Access Policy Helper

A BigQuery Remote function to query and view row-level access policies since Row Level Access Policies are currently viewable via the API and `bq` CLI.

## Summary

The workflow is as follows:

* Setup GCP environment - enable APIs, BQ connection
* Setup data in BigQuery - load data and implement example row-level security policies
* Setup Google Cloud function - Python function to call the BQ API (`rowAccessPolicies` method)
* Create BigQuery UDF - from Google Cloud Function  
* Use BigQuery UDF - to get rowAccessPolicies within SQL 


## Getting Started

To begin, follow the steps below in Cloud Shell and/or the Cloud Console. To clone this repository and work directly in Cloud Shell (recommended), click the buttom below:

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://shell.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/justinjm/gcp-bigquery-row-level-access)


## Setup GCP environment 

### Enable apis

```sh
gcloud services enable bigqueryconnection.googleapis.com
```

### Setup connection

```sh
gcloud components update
bq mk --connection --display_name='get_row_access_policies' --connection_type=CLOUD_RESOURCE --project_id=$(gcloud config get-value project) --location=US  gcf-conn
```

Show connection info and copy service account, you will need this in a later step

```sh
bq show --location=US --connection gcf-conn
```

## Setup BigQuery 

### Load Data

Create a BQ dataset and then load the 2 example csv files from this repository into 2 BQ tables

```sh
bq mk -d z_test 
```

```sh
# bq load crm_account.csv
```

```sh
# bq load crm_users.csv
```

Then, create row level access policies for each table 

1. crm_account_rsl

```sql
CREATE ROW ACCESS POLICY crm_account_filter
ON `demos-vertex-ai.z_test.crm_account_rsl`
GRANT TO('user:bruce@justinjm.altostrat.com')
FILTER USING(State_Code='CA')
```

2. crm_user_rsl

```sql
CREATE ROW ACCESS POLICY crm_user_filter
ON `demos-vertex-ai.z_test.crm_user_rsl`
GRANT TO('user:bruce@justinjm.altostrat.com')
FILTER USING(Country_Code = 'US')
```

## Setup Google Cloud Function

Navigate to [Cloud Functions](https://console.cloud.google.com/functions) within the Google Cloud console and setup a Cloud function as follows: 

* Cloud function v1
* type = https
* leave the rest as defaults and click next 
* In the source tab, copy `main.py` 
* change entry point to `get_row_access_polices`
* click deploy

### Grant service accounts acccess

While GCF is deploying, grant account access in 2 places

1. the app engine default service account BigQuery permissions (you can remove/adjust this later) so that the cloud

```sh
gcloud projects add-iam-policy-binding demos-vertex-ai \
    --member=serviceAccount:demos-vertex-ai@appspot.gserviceaccount.com \
    --role=roles/bigquery.admin
```

2. Grant

```sh
gcloud functions add-iam-policy-binding bq-table-row-access-policies \
    --member=serviceAccount:bqcx-746038361521-agnk@gcp-sa-bigquery-condel.iam.gserviceaccount.com \
    --role=roles/cloudfunctions.invoker
```

### Test Cloud Function 

After deployment completes, test with sample values:

```txt
{
  "calls": [
      ["your-project-id", "z_test", "crm_account"]
      ["your-project-id", "z_test", "crm_user"]
  ]
}
```

You should see a repsonse with the `rowAccessPolicies` as the main object. 

## Create BigQuery UDF

Now, navigate to BigQuery UI and run the following SQL to create a BigQuery UDF 

```sql
CREATE OR REPLACE FUNCTION
  z_test.get_row_access_policies(table_catalog STRING,
    table_schema STRING,
    table_name STRING)
  RETURNS STRING REMOTE
  -- change this to reflect your PROJECT ID
WITH CONNECTION `demos-vertex-ai.us.gcf-conn` OPTIONS (
    -- change this to reflect the Trigger URL of your cloud function (look for the TRIGGER tab)
    endpoint = 'https://us-central1-demos-vertex-ai.cloudfunctions.net/bq-table-row-access-policies' )
```

## Invoke remote function from BigQuery

Finally, use the UDF (and Remote Function) in a SQL query from the `INFORMATION_SCHEMA`: 

```sql
SELECT
  table_catalog,
  table_schema,
  table_name,
  `z_test`.get_row_access_policies(table_catalog, table_schema, table_name) as rowAccessPolicies
FROM
  z_test.INFORMATION_SCHEMA.TABLES
```

A more robust query to format the raw JSON response into columns: 

```sql
WITH data AS (
  SELECT
  table_catalog,
  table_schema,
  table_name,
  `z_test`.get_row_access_policies(table_catalog, table_schema, table_name) as reply
FROM
  z_test.INFORMATION_SCHEMA.TABLES
) 
SELECT
  * EXCEPT(reply),
  REPLACE(JSON_QUERY(reply, '$.rowAccessPolicies[0].rowAccessPolicyReference.policyId'), '"', '') AS policyId,
  REPLACE(JSON_QUERY(reply, '$.rowAccessPolicies[0].filterPredicate'), '"', '') AS filterPredicate,
  REPLACE(JSON_QUERY(reply, '$.rowAccessPolicies[0].creationTime'), '"', '') AS creationTime,
  REPLACE(JSON_QUERY(reply, '$.rowAccessPolicies[0].lastModifiedTime'), '"', '') AS lastModifiedTime

FROM data
```

<https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#string_for_json>

## Resources

BigQuery Row Level Security

* [Use row-level security  |  BigQuery  |  Google Cloud](https://cloud.google.com/bigquery/docs/managing-row-level-security#bq)
* [Method: rowAccessPolicies.list  |  BigQuery  |  Google Cloud](https://cloud.google.com/bigquery/docs/reference/rest/v2/rowAccessPolicies/list#RowAccessPolicy)
* [HTTP Tutorial  |  Cloud Functions Documentation  |  Google Cloud](https://cloud.google.com/functions/docs/tutorials/http-1st-gen)

BigQuery Remote Functions

* [Working with Remote Functions  |  BigQuery  |  Google Cloud](https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#sample_code)
* [Remote Functions in BigQuery. How it works, and what you can do with… | by Lak Lakshmanan | Towards Data Science](https://towardsdatascience.com/remote-functions-in-bigquery-af9921498438) - good tutorial by former Googler

BigQuery Information Schema

* [TABLES view  |  BigQuery  |  Google Cloud](https://cloud.google.com/bigquery/docs/information-schema-tables)
