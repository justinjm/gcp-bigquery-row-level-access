# Stress test

Notes on stress test of calling `rowAccessPolicies` 10,000 times in one run.

## Steps followed 

### 1. Setup BigQuery Remote Function 

Follow setup steps in `README.md` to setup BigQuery Remote Function

### 2. Create sample data and upload to bigquery 

via `tests/create-sample-bq-table.py` for the large stress test of 10k API calls 

### 3. Create small and medium  sample datasets

Before running major stress test of 10k, create 2 samples for a small and medium stress

1. 100
2. 1000
 
#### 3.1 Create small table of 100

```sql
CREATE OR REPLACE TABLE
  `z_test.z_sample_info_schema_input100` AS (
  SELECT * FROM `z_test.z_sample_info_schema_input` LIMIT 100)
```

#### 3.2  Create medium table of 1000

```sql
CREATE OR REPLACE TABLE
  `z_test.z_sample_info_schema_input1000` AS (
  SELECT * FROM `z_test.z_sample_info_schema_input` LIMIT 1000)
```

### 3. run stress tests

now we run the stress tests, manually one at a time and increasing the number of 
API requests each time (100 --> 1000 --> 10,000)

#### query for 100 tables

```sql
SELECT
  table_catalog,
  table_schema,
  table_name,
  `z_test`.get_row_access_policies(table_catalog, table_schema, table_name) as rowAccessPolicies
FROM
  z_test.z_sample_info_schema_input100
```

#### query for 1k tables

```sql
SELECT
  table_catalog,
  table_schema,
  table_name,
  `z_test`.get_row_access_policies(table_catalog, table_schema, table_name) as rowAccessPolicies
FROM
  z_test.z_sample_info_schema_input1000
```

#### query for 10k tables

```sql
SELECT
  table_catalog,
  table_schema,
  table_name,
  `z_test`.get_row_access_policies(table_catalog, table_schema, table_name) as rowAccessPolicies
FROM
  z_test.z_sample_info_schema_input
```
