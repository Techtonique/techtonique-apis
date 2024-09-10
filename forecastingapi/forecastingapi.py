import requests
from .config import BASE_URL


def read_file_or_url(file_name, path):
    if path.startswith("http://") or path.startswith("https://"):
        response = requests.get(path)
        return {file_name: response.content}
    else:
        return {file_name: open(path, "rb")}


def get_forecast(
    file,
    token,
    endpoint="forecastinggbdt",
    method="RidgeCV",
    n_hidden_features=5,
    lags=25,
    type_pi='gaussian',
    h=10,
):
    headers = {'Authorization': 'Bearer ' + token}

    params = {
    'method': method,
    'n_hidden_features': str(n_hidden_features),
    'lags': str(lags),
    'type_pi': type_pi,
    'h': str(h),
    }

    try:
        
        response_forecast = requests.post(
            BASE_URL + "/" + str(endpoint),
            files=read_file_or_url("file", file),
            params=params,
            headers=headers,
        )

    except Exception as e:
        print(e)
        return {
            "status": 400,
            "message": "Please check the token + the file is in the right format (csv, txt, or json) + the url is correct.",
        }

    return response_forecast.json()
