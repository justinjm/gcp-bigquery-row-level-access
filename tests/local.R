source("tests/functions.R")

email <- Sys.getenv("GAR_AUTH_EMAIL")
projectId <- Sys.getenv("PROJECT")
datasetId <- Sys.getenv("DATASET")
tableId <- Sys.getenv("TABLE")

options(googleAuthR.scopes.selected = "https://www.googleapis.com/auth/cloud-platform")
options(googleAuthR.verbose = 0) # set when debugging
# options(gargle_verbosity = "debug") # set when debugging

library(googleAuthR)

gar_auth(email = Sys.getenv("GARGLE_AUTH_EMAIL"))

## confirm auth successful with simple api calls
# bq_project_datasets(projectId)
# rls <- get_rls_policies(projectId, datasetId, tableId)
# rls$rowAccessPolicies

# function ---------------------------------------------------------------------
stress_test <- function(projectId,
                        datasetId,
                        tableId,
                        num_rows){
  df <- data.frame(
    table_catalog = rep(projectId, num_rows),
    table_schema = rep(datasetId, num_rows),
    table_name = rep(tableId, num_rows)
  )
  start.time <- Sys.time()
  result <- apply(df, 1, function(row) get_rls_policies(
    row["table_catalog"], row["table_schema"], row["table_name"])
    )

  end.time <- Sys.time()
  time.taken <- as.numeric(end.time - start.time, units = "secs")
  print(paste("Time taken: ", time.taken, "seconds"))
  return(result)
}

results <- stress_test(projectId, datasetId, tableId, num_rows = 10000)
length(results)


# gar_debug_parsing(filename = "gar_parse_error.rds")

# https://cran.r-project.org/web/packages/gargle/vignettes/troubleshooting.html
# https://cloud.google.com/bigquery/docs/reference/rest/v2/rowAccessPolicies/list?apix=true
