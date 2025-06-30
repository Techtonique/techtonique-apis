import os
from dotenv import load_dotenv
import getpass
import requests
import ast

from typing import Optional, Dict, Any, Union
from .config import BASE_URL, get_token


class TechtoniqueAPI:

    def __init__(self):
        self.token = get_token()
        self.BASE_URL = BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }

    def _post_file(
        self,
        endpoint: str,
        file_path: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Send a POST request with a file upload."""
        url = f"{self.BASE_URL}{endpoint}"
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f, "text/csv")}
            response = requests.post(url, headers=self.headers,
                                     files=files, params=params)
        response.raise_for_status()
        return response.json()

    def _get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Send a GET request."""
        url = f"{self.BASE_URL}{endpoint}"
        headers = self.headers.copy()
        headers["accept"] = "application/json"
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    # 1 - Forecasting -----

    def forecasting(
        self,
        file_path: str,
        base_model: str = "RidgeCV",
        n_hidden_features: int = 5,
        lags: int = 25,
        type_pi: str = "kde",
        replications: int = 10,
        h: int = 5,
    ) -> Dict[str, Any]:
        params = {
            "base_model": base_model,
            "n_hidden_features": n_hidden_features,
            "lags": lags,
            "type_pi": type_pi,
            "replications": replications,
            "h": h,
        }
        return self._post_file("/forecasting", file_path, params)

    # 2 - Machine Learning  -----

    def mlclassification(
        self,
        file_path: str,
        base_model: str = "RandomForestClassifier",
        n_hidden_features: int = 5,
        predict_proba: bool = False,
    ) -> Dict[str, Any]:
        params = {
            "base_model": base_model,
            "n_hidden_features": n_hidden_features,
            "predict_proba": str(predict_proba).lower(),
        }
        return self._post_file("/mlclassification", file_path, params)

    def mlregression(
        self,
        file_path: str,
        base_model: str = "ElasticNet",
        n_hidden_features: int = 5,
        return_pi: bool = True,  # default True as in example
    ) -> Dict[str, Any]:
        params = {
            "base_model": base_model,
            "n_hidden_features": n_hidden_features,
            "return_pi": str(return_pi).lower(),
        }
        return self._post_file("/mlregression", file_path, params)

    def gbdt_regression(
        self,
        file_path: str,
        model_type: str = "lightgbm",
        return_pi: bool = False,
    ) -> Dict[str, Any]:
        params = {
            "model_type": model_type,
            "return_pi": str(return_pi).lower(),
        }
        return self._post_file("/gbdtregression", file_path, params)

    def gbdt_classification(
        self,
        file_path: str,
        model_type: str = "lightgbm",
    ) -> Dict[str, Any]:
        params = {
            "model_type": model_type,
        }
        return self._post_file("/gbdtclassification", file_path, params)

    # 3 - Reserving -----

    def reserving(
        self,
        file_path: str,
        method: str = "chainladder",  # default as in example
    ) -> Dict[str, Any]:
        params = {"method": method}
        return self._post_file("/reserving", file_path, params)

    def mlreserving(
        self,
        file_path: str,
        method: str = "RidgeCV",
    ) -> Dict[str, Any]:
        params = {"method": method}
        return self._post_file("/mlreserving", file_path, params)

    # 4 - Survival Analysis -----

    def survival_curve(
        self,
        file_path: str,
        method: str = "km",  # default as in example
        patient_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        params = {"method": method}
        if patient_id is not None:
            params["patient_id"] = patient_id
        return self._post_file("/survivalcurve", file_path, params)

    # 5 - Simulation -----

    def simulate_scenario(
        self,
        model: str = "GBM",  # default as in example
        n: int = 10,
        horizon: int = 5,
        frequency: str = "quarterly",
        x0: Optional[Union[int, float]] = 1.0,  # required for GBM, default 1.0
        theta1: Optional[float] = 0.0,
        theta2: Optional[float] = 0.5,
        theta3: Optional[float] = None,
        seed: Optional[int] = None,
    ) -> Dict[str, Any]:
        params = {
            "model": model,
            "n": n,
            "horizon": horizon,
            "frequency": frequency,
        }
        if x0 is not None:
            params["x0"] = x0
        if theta1 is not None:
            params["theta1"] = theta1
        if theta2 is not None:
            params["theta2"] = theta2
        if theta3 is not None:
            params["theta3"] = theta3
        if seed is not None:
            params["seed"] = seed
        return self._get("/scenarios/simulate/", params)
