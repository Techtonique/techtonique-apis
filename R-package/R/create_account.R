
#' Create an account for using Techtonique APIs
#'
#' @param username a string; your username
#' @param password a string; your password
#'
#' @return
#' @export
#'
create_account <- function(username, password)
{
  base_url <- "https://techtonique2.herokuapp.com"

  if (is.character(username) == FALSE)
    stop("'username' must be a string")

  if (is.character(password) == FALSE)
    stop("'password' must be a string")

  headers = c(
    `Content-Type` = 'application/json'
  )

  data <- jsonlite::toJSON(list(username = username, password = password),
                           auto_unbox = TRUE)

  res <- httr::POST(url = paste0(base_url, '/api/users'),
                    config = httr::add_headers(.headers=headers),
                    body = data)

  print(res)

  return(res)
}
