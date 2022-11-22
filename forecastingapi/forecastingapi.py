"""Main module."""

import requests

base_url = 'https://techtonique2.herokuapp.com'


def create_account(username, password):

    headers = {
    # Already added when you pass json=
    # 'Content-Type': 'application/json',
    }

    json_data = {
        'username': str(username),
        'password': str(password),
    }

    response = requests.post(base_url + '/api/users', headers=headers, json=json_data)

    return response


def get_token(username, password):

    response_token = requests.get(base_url + '/api/token', 
    auth=(str(username), str(password)))

    token = response_token.json()['token']

    return token


def get_forecast(file, token,
                method = "theta", # currently "theta", "mean", "rw", "prophet"
                h = 5, level = 95, 
                date_formatting = "original", # either "original" (yyyy-mm-dd) or "ms" (milliseconds)
                start_training = None, n_training = None):

    if ((start_training is not None) and (n_training is not None)):

        params = {
        'h': str(h),
        'level': str(level),
        'date_formatting': str(date_formatting),
        'start_training': str(start_training), 
        'n_training': str(n_training)
        }
    
    else:

        params = {
        'h': str(h),
        'level': str(level),
        'date_formatting': str(date_formatting),
        }

    files = {
    'file': open(str(file), 'rb') # Example files available at https://github.com/Techtonique/datasets/tree/main/time_series/univariate
    }

    response_forecast = requests.post(base_url + '/api/' + str(method), 
    files=files, params=params, auth=(token, 'x'))

    return response_forecast.json()


