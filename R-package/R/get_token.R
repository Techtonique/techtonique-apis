

#' Obtain a token, for use in API requests
#'
#' @param username a string; your username
#' @param password a string; your password
#'
#' @return a string; the token used in API requests (function \code{get_forecast} of this package)
#' @export
#'
get_token <- function(username, password){

  base_url <- "https://techtonique2.herokuapp.com"

  if (is.character(username) == FALSE)
    stop("'username' must be a string")

  if (is.character(password) == FALSE)
    stop("'password' must be a string")

  res_token <- httr::GET(url = paste0(base_url, '/api/token'),
                         httr::authenticate(username, password))

  print(res_token)

  return(httr::content(res_token)$token)
}
