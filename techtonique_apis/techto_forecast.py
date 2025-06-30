import tempfile
import datetime as dt
import numpy as np
import pandas as pd
#import seaborn as sns
from xlwings import func, arg, ret
from .techtonique_apis import TechtoniqueAPI


api = TechtoniqueAPI()

def excel_date_to_datetime(excel_serial):
    # Excel's day 0 is 1899-12-30
    return pd.to_datetime('1899-12-30') + pd.to_timedelta(excel_serial, unit='D')

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
    return_sims: bool = False 
) -> pd.DataFrame:
    """Forecasting: pass a time series as a DataFrame from Excel, return forecast.
    
    Excel/xlwings custom function: Forecast a time series passed as a DataFrame from Excel, using the Techtonique API.

    Parameters
    ----------

    df : pd.DataFrame
        The input time series data as a DataFrame (from Excel range).

    base_model : str, default "RidgeCV"
        The base model to use for forecasting.

    n_hidden_features : int, default 5
        Number of hidden features for the model.

    lags : int, default 25
        Number of lags to use in the model.

    type_pi : str, default "kde"
        Type of prediction interval ("kde" or other supported types).

    replications : int, default 10
        Number of simulation replications.

    h : int, default 5
        Forecast horizon (number of periods ahead to forecast).

    return_sims : bool, default False
        If True, return the simulation matrix; otherwise, return the forecast summary bounds.

    Returns
    -------

    pd.DataFrame
        The forecast results or simulation matrix as a DataFrame for Excel.
        
    """
    # Convert Excel serial dates to datetime if needed
    if pd.api.types.is_numeric_dtype(df['date']):
        df['date'] = df['date'].apply(excel_date_to_datetime)

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
    output_dates = result["date"]
    res_df = pd.DataFrame(result.pop('sims'))
    if return_sims:
        res2_df = pd.DataFrame([])
        res2_df["date"] = output_dates
        sims_df = res_df.transpose()
        sims_df.columns = [(i + 1) for i in range(sims_df.shape[1])]
        return pd.concat([res2_df, sims_df], axis=1)
    return pd.DataFrame(result)

