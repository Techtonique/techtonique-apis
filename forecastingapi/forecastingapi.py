import requests
from .config import BASE_URL


def get_forecast(
    path_to_file,
    base_model="RidgeCV",
    n_hidden_features=5,
    lags=25,
    type_pi="gaussian",
    replications=None,
    h=10,
):
    """
    Get a forecast from the Techtonique API.

    Parameters:
    -----------

    path_to_file : str
        Path to the input file or URL containing the time series data.

    base_model : str
        Forecasting method to use (default is "RidgeCV"); for now scikit-learn model names. 

    n_hidden_features : int
        Number of hidden features for the model (default is 5).

    lags : int
        Number of lags to use in the model (default is 25).

    type_pi : str
        Type of prediction interval to use (default is 'gaussian').

    replications : int
        Number of replications for certain methods (default is None).

    h : int
        Forecast horizon (default is 10).

    Returns:
    --------
    dict
        A dictionary containing the forecast results (mean, lower bound, upper bound, and simulations).

    Example:
    --------   
    >>> from forecastingapi import get_forecast
    >>> # path to your local timeseries data (examples in https://github.com/Techtonique/datasets/tree/main/time_series)
    >>> file_path = "path/to/your/timeseries/data.csv"
    >>> forecast = get_forecast(file_path, h=15)
    >>> print(forecast)
    """

    token = input("Enter your token (from https://www.techtonique.net/token): ")

    headers = {
        'Authorization': 'Bearer ' + token,
    }

    params = {
        'base_model': str(base_model),
        'n_hidden_features': str(n_hidden_features),
        'lags': str(lags),
        'type_pi': str(type_pi),
        'replications': str(replications),
        'h': str(h),
    }

    files = {
        'file': (path_to_file, read_file_or_url(path_to_file), 'text/csv'),
    }

    response = requests.post(BASE_URL + '/forecasting',
                             params=params, headers=headers, files=files)

    return response.json()


def read_file_or_url(path):
    if path.startswith("http://") or path.startswith("https://"):
        response = requests.get(path)
        return response.content
    else:
        return open(path, "rb")
