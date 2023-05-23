#' 
get_rls_policies <- function(projectId,
                             datasetId,
                             tableId) {
  
  
  url <- sprintf("https://bigquery.googleapis.com/bigquery/v2/projects/%s/datasets/%s/tables/%s/rowAccessPolicies",
                 projectId,
                 datasetId,
                 tableId)
  
  
  f <- googleAuthR::gar_api_generator(url,
                                      "GET",
                                      data_parse_function = function(x) x,
                                      checkTrailingSlash = TRUE)

  response <- f()

  response
  
  
}