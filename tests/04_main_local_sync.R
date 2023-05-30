# set constants 
email <- Sys.getenv("GAR_AUTH_EMAIL")
projectId <- Sys.getenv("PROJECT")
datasetId <- Sys.getenv("DATASET")
tableId <- Sys.getenv("TABLE")

# authentication ---------------------------------------------------------------
# set options for auth and debugging if needed
options(googleAuthR.scopes.selected = "https://www.googleapis.com/auth/cloud-platform")
# options(googleAuthR.verbose = 0) # set when debugging

## authenticate 
library(googleAuthR)
gar_auth(email = Sys.getenv("GARGLE_AUTH_EMAIL"))

## confirm auth successful with simple api calls
rls <- get_rls_policies(projectId, datasetId, tableId)
rls$rowAccessPolicies

# function ---------------------------------------------------------------------
get_rls_policies <- function(projectId,
                             datasetId,
                             tableId) {
  url <- sprintf(
    "https://bigquery.googleapis.com/bigquery/v2/projects/%s/datasets/%s/tables/%s/rowAccessPolicies",
    projectId,
    datasetId,
    tableId
  )

  f <- googleAuthR::gar_api_generator(url,
    "GET",
    data_parse_function = function(x) x,
    checkTrailingSlash = TRUE
  )

  response <- f()

  response
}


# stress test -----------------------------------------------------------------
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
  
  counter <- 1
  result <- apply(df, 1, function(row) {
    cat("[?] Row number: ", counter, "======================================\n")
    counter <<- counter + 1
    get_rls_policies(row["table_catalog"],row["table_schema"],row["table_name"])
  }
  )
  
  end.time <- Sys.time()
  time.taken <- as.numeric(end.time - start.time, units = "secs")
  print(paste("Time taken: ", time.taken, "seconds"))
  print(paste("Number of API calls:", counter - 1))
  return(result)
}

# execute  ---------------------------------------------------------------------
results <- stress_test(projectId, datasetId, tableId, num_rows = 10000)
length(results)

## save results for sharing
outfile <- paste0("data/results-", format(Sys.time(), "%Y%m%d%H%M%S"), ".rds")
saveRDS(results, outfile)

## Debug 
# gar_debug_parsing(filename = "gar_parse_error.rds")

## references
# https://cran.r-project.org/web/packages/gargle/vignettes/troubleshooting.html
# https://cloud.google.com/bigquery/docs/reference/rest/v2/rowAccessPolicies/list?apix=true
# https://www.r-bloggers.com/2021/08/r-a-combined-usage-of-split-lapply-and-do-call/