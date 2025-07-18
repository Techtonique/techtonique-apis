import tempfile
import datetime as dt
import numpy as np
import pandas as pd
import seaborn as sns
from xlwings import func, arg, ret
from techtonique_apis import TechtoniqueAPI


api = TechtoniqueAPI()

@func
def hello(name: str):
    # This is the easiest custom function
    return f"Hello {name}!"


@func
def standard_normal(rows, cols):
    # Returns an array of standard normally distributed pseudo random numbers
    rng = np.random.default_rng()
    matrix = rng.standard_normal(size=(rows, cols))
    date_rng = pd.date_range(start=dt.datetime(2025, 6, 15), periods=rows, freq="D")
    df = pd.DataFrame(
        matrix, columns=[f"col{i + 1}" for i in range(matrix.shape[1])], index=date_rng
    )
    return df


@func
def correl2(df: pd.DataFrame):
    # Like CORREL, but it works on whole matrices instead of just 2 arrays.
    # The type hint converts the values of the range into a pandas DataFrame.
    # Use this function on the output of the standard_normal function from above.
    return df.corr()

@func
@arg("df", index=False)
@ret(index=False)
def techto_forecast(
    df: pd.DataFrame,
    base_model: str = "RidgeCV",
    n_hidden_features: int = 5,
    lags: int = 25,
    type_pi: str = "kde",
    replications: int = 10,
    h: int = 5,
) -> pd.DataFrame:
    """Forecasting: pass a time series as a DataFrame from Excel, return forecast."""
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        df.to_csv(tmp.name, index=False)
        result = api.forecasting(
            file_path=tmp.name,
            base_model=base_model,
            n_hidden_features=n_hidden_features,
            lags=lags,
            type_pi=type_pi,
            replications=replications,
            h=h,
        )
    print("Forecasting result:", result)
    #forecast = result.get("forecast", [])
    #return pd.DataFrame(forecast)

@func
@arg("df", index=False)
@ret(index=False)
def techto_regression(
    df: pd.DataFrame,
    base_model: str = "ElasticNet",
    n_hidden_features: int = 5,
    return_pi: bool = True,
) -> pd.DataFrame:
    """Regression: pass a tabular dataset as a DataFrame from Excel, return predictions."""
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        df.to_csv(tmp.name, index=False)
        result = api.mlregression(
            file_path=tmp.name,
            base_model=base_model,
            n_hidden_features=n_hidden_features,
            return_pi=return_pi,
        )
    print("Regression result:", result)
    #predictions = result.get("predictions", [])
    #return pd.DataFrame(predictions)

@func
@arg("df", index=False)
@ret(index=False)
def techto_gbdt_classification(
    df: pd.DataFrame,
    model_type: str = "lightgbm"
) -> pd.DataFrame:
    """GBDT Classification: pass a classification dataset as a DataFrame from Excel, return predictions."""
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        df.to_csv(tmp.name, index=False)
        result = api.gbdt_classification(
            file_path=tmp.name,
            model_type=model_type,
        )
    print("GBDT Classification result:", result)
    #predictions = result.get("predictions", [])
    #return pd.DataFrame(predictions)

@func
@arg("df", index=False)
@ret(index=False)
def techto_reserving(
    df: pd.DataFrame,
    method: str = "chainladder"
) -> pd.DataFrame:
    """Reserving: pass a triangle dataset as a DataFrame from Excel, return reserving results."""
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        df.to_csv(tmp.name, index=False)
        result = api.reserving(
            file_path=tmp.name,
            method=method,
        )
    print("Reserving result:", result)
    # Adjust the key as needed based on API response
    #reserving = result.get("reserving", [])
    #return pd.DataFrame(reserving)

@func
@arg("df", index=False)
@ret(index=False)
def techto_survival_curve(
    df: pd.DataFrame,
    method: str = "km",
    patient_id: int = None
) -> pd.DataFrame:
    """Survival analysis: pass a survival dataset as a DataFrame from Excel, return survival curve."""
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        df.to_csv(tmp.name, index=False)
        result = api.survival_curve(
            file_path=tmp.name,
            method=method,
            patient_id=patient_id,
        )
    print("Survival curve result:", result)
    #survival = result.get("survival_curve", [])
    #return pd.DataFrame(survival)

@func
def techto_simulate_scenario(
    model: str = "GBM",
    n: int = 10,
    horizon: int = 5,
    frequency: str = "quarterly",
    x0: float = 100,
    theta1: float = 0,
    theta2: float = 0.5,
    theta3: float = 0.5,
    seed: int = None,
) -> pd.DataFrame:
    """Simulate scenario and return simulated values as a DataFrame for Excel."""
    result = api.simulate_scenario(
        model=model,
        n=n,
        horizon=horizon,
        frequency=frequency,
        x0=x0,
        theta1=theta1,
        theta2=theta2,
        theta3=theta3,
        seed=seed,
    )
    print("Simulation result:", result)
    #simulated = result.get("simulated", [])
    #return pd.DataFrame(simulated)    
