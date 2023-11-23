import requests
from .config import BASE_URL


def create_account(username, password):
    headers = {
        # Already added when you pass json=
        # 'Content-Type': 'application/json',
    }

    json_data = {
        "username": str(username),
        "password": str(password),
    }

    response = requests.post(
        BASE_URL + "/api/users", headers=headers, json=json_data
    )

    return response


def get_token(username, password):
    response_token = requests.get(
        BASE_URL + "/api/token", auth=(str(username), str(password))
    )

    token = response_token.json()["token"]

    return token


def read_file_or_url(file_name, path):
    if path.startswith("http://") or path.startswith("https://"):
        response = requests.get(path)
        return {file_name: response.content}
    else:
        return {file_name: open(path, "rb")}


def get_forecast(
    file,
    token,
    method="theta",  # currently "theta", "mean", "rw", "prophet"
    h=5,
    level=95,
    date_formatting="original",  # either "original" (yyyy-mm-dd) or "ms" (milliseconds)
    start_training=None,
    n_training=None,
):
    if (start_training is not None) and (n_training is not None):
        params = {
            "h": str(h),
            "level": str(level),
            "date_formatting": str(date_formatting),
            "start_training": str(start_training),
            "n_training": str(n_training),
        }

    else:
        params = {
            "h": str(h),
            "level": str(level),
            "date_formatting": str(date_formatting),
        }

    try:
        response_forecast = requests.post(
            BASE_URL + "/api/" + str(method),
            files=read_file_or_url("file", file),
            params=params,
            auth=(token, "x"),
        )

    except Exception as e:
        print(e)
        return {
            "status": 400,
            "message": "Please check the token + the file is in the right format (csv, txt, or json) + the url is correct.",
        }

    return response_forecast.json()
