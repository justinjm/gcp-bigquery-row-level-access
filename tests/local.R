source("tests/functions.R")

email <- Sys.getenv("GAR_AUTH_EMAIL")
projectId <- Sys.getenv("PROJECT")
datasetId <- Sys.getenv("DATASET")
tableId <- Sys.getenv("TABLE")

options(googleAuthR.scopes.selected = "https://www.googleapis.com/auth/cloud-platform")
options(googleAuthR.verbose = 0) # set when debugging
# options(gargle_verbosity = "debug")

library(googleAuthR)

gar_auth(email = Sys.getenv("GARGLE_AUTH_EMAIL"))

# bq_project_datasets(projectId)
# 

rls <- get_rls_policies(projectId, datasetId, tableId)
rls$rowAccessPolicies

# https://cran.r-project.org/web/packages/gargle/vignettes/troubleshooting.html
# https://cloud.google.com/bigquery/docs/reference/rest/v2/rowAccessPolicies/list?apix=true

# Specify the number of rows in the dataframe then build it
num_rows <- 100
df <- data.frame(
  table_catalog = rep("demos-vertex-ai", num_rows),
  table_schema = rep("z_test", num_rows),
  table_name = rep("crm_account", num_rows)
)

# Let's assume this is our function
# my_function <- function(x, y, z) {
#   # This function will just add the three inputs
#   print(x)
#   print(y)
#   print(z)
#   cat("=================\n")
# }
# apply(df, 1, function(row) my_function(row['table_catalog'], row['table_schema'], row['table_name']))

result <- apply(df, 1, function(row) get_rls_policies(row['table_catalog'], row['table_schema'], row['table_name']))
result

