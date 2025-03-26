import os
from dotenv import load_dotenv
import getpass
import requests
from .config import BASE_URL


def get_token(token=None):
    """
    Retrieve the API token, either from the environment or user input.

    Parameters:
    -----------
    token : str
        Token provided as a parameter (default is None).

    Returns:
    --------
    str
        A valid API token.
    """
    if token:
        return token

    # Load environment variables from .env if available
    load_dotenv()
    token = os.getenv("TECHTONIQUE_TOKEN")

    if not token:
        # Prompt user for token if not found in environment
        token = getpass.getpass("Enter your token (from https://www.techtonique.net/token): ")

    if not token:
        raise ValueError("API token is required but was not provided.")

    return token

def get_forecast(
    path_to_file,
    base_model="RidgeCV",
    n_hidden_features=5,
    lags=25,
    type_pi="gaussian",
    replications=None,
    h=10,
    token=None,
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
    
    token : str
        API token for authentication (default is None). If not provided, and if not in the environment, the user will be prompted to enter it.

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

    token = get_token(token)

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
