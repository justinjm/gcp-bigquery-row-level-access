source("functions.R")

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

get_rls_policies(projectId, datasetId, tableId)


# https://cran.r-project.org/web/packages/gargle/vignettes/troubleshooting.html
# https://cloud.google.com/bigquery/docs/reference/rest/v2/rowAccessPolicies/list?apix=true