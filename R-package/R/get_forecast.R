

#' Obtain forecasts from a csv file
#'
#' @param file a string; path to csv file containing time series data (examples:
#' https://github.com/Techtonique/datasets/tree/main/time_series/univariate)
#' @param token a string; authentication token (obtained with \code{forecastingAPI::get_token})
#' @param method a string; forecasting method (currently Theta, mean forecast, Random walk forecasting,
#' and FB Prophet forecasting)
#' @param h an integer; number of periods for forecasting
#' @param level an integer; confidence levels for prediction intervals
#' @param date_formatting a string; either "original" (yyyy-mm-dd) or "ms" (milliseconds)
#' @param start_training an integer; starting index for training window
#' @param n_training an integer; length of training window
#'
#' @return a list of "averages" (mean forecast) and "ranges" (lower and upper bounds of prediction interval)
#' @export
#'
get_forecast <- function(file, token,
                         method = c("theta", "mean", "rw", "prophet"),
                         h = 5, level = 95,
                         date_formatting = "original",
                         start_training = NULL, n_training = NULL)
{
  base_url <- "https://techtonique2.herokuapp.com"

  method <- match.arg(method)

  if(!is.null(start_training) && !is.null(n_training))
  {
    params = list(
      `h` = as.character(h), # horizon
      `level` = as.character(level), # level of confidence for prediction intervals
      `date_formatting` = as.character(date_formatting),
      `start_training` = as.character(start_training),
      `n_training` = as.character(n_training)
    )
  } else {
    params = list(
      `h` = as.character(h), # horizon
      `level` = as.character(level), # level of confidence for prediction intervals
      `date_formatting` = as.character(date_formatting)
    )
  }

  if (grepl("^(http|https)://", file)) {
    temp_file <- tempfile()    
    httr::GET(file, httr::write_disk(temp_file, overwrite = TRUE))
    if (!file.exists(temp_file)) {
      stop("Failed to download file")
    }
    file <- temp_file    
  }

  files = list(
    `file` = httr::upload_file(file)
  )

  res_forecast <- httr::POST(url = paste0(base_url, '/api/', method),
                             query = params, body = files, encode = 'multipart',
                             httr::authenticate(token, 'x'))

  print(res_forecast)

  return(httr::content(res_forecast))
}
