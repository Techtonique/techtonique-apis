import tempfile
import datetime as dt
import numpy as np
import pandas as pd
# import seaborn as sns
from xlwings import func, arg, ret
from .techtonique_apis import TechtoniqueAPI


api = TechtoniqueAPI()


def excel_date_to_datetime(excel_serial):
    # Excel's day 0 is 1899-12-30
    return pd.to_datetime('1899-12-30') + pd.to_timedelta(excel_serial, unit='D')


@func
@arg("df", index=False, doc="Excel range with columns 'date' and one or more series.")
@arg("base_model", doc='Forecasting model (default: "RidgeCV")')
@arg("n_hidden_features", doc="Number of hidden features (default: 5)")
@arg("lags", doc="Number of lags (default: 25)")
@arg("type_pi", doc='Prediction interval type (default: "kde")')
@arg("replications", doc="Number of simulation replications (default: 10)")
@arg("h", doc="Forecast horizon (default: 5)")
@arg("return_sims", doc="If TRUE, return simulation matrix; else, return forecast summary (default: FALSE)")
@arg("series_choice", doc="(Optional) Name of the series to forecast if multiple are present")
@ret(index=False, doc="Forecast or simulation results as a table for Excel")
def techto_forecast(
    df: pd.DataFrame,
    base_model: str = "RidgeCV",
    n_hidden_features: int = 5,
    lags: int = 25,
    type_pi: str = "kde",
    replications: int = 10,
    h: int = 5,
    return_sims: bool = False,
    series_choice: str = None
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

    series_choice : str, optional
        If provided, specifies which series to forecast from the DataFrame.

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
    if df.shape[1] == 2:  # univariate time series
        res_df = pd.DataFrame(result.pop('sims'))
        if return_sims:
            res2_df = pd.DataFrame([])
            res2_df["date"] = output_dates
            sims_df = res_df.transpose()
            sims_df.columns = [(i + 1) for i in range(sims_df.shape[1])]
            return pd.concat([res2_df, sims_df], axis=1)
        return pd.DataFrame(result)
    else:  # multivariate time series
        n_series = len(result["mean"][0])
        series_names = [col for col in df.columns if col != "date"]
        if len(series_names) != n_series:
            series_names = [f"series_{i+1}" for i in range(n_series)]

        # If series_choice is provided and valid, extract its index and return as univariate
        if series_choice is not None and series_choice in series_names:
            idx = series_names.index(series_choice)
            # Extract only the selected series from each stat
            summary_df = pd.DataFrame({
                "date": output_dates,
                "mean": [x[idx] for x in result["mean"]],
                "lower": [x[idx] for x in result["lower"]],
                "upper": [x[idx] for x in result["upper"]],
            })
            if return_sims:
                # sims: shape (replications, horizon, n_series)
                # list of replications, each is list of horizon, each is list of n_series
                sims = result["sims"]
                # For each replication, extract the selected series only
                sims_selected = [[h[idx] for h in rep]
                                 for rep in sims]  # shape: (replications, horizon)
                sims_df = pd.DataFrame(sims_selected).transpose()
                sims_df.columns = [
                    f"sim_{i+1}_{series_choice}" for i in range(sims_df.shape[1])]
                res2_df = pd.DataFrame({"date": output_dates})
                return pd.concat([res2_df, sims_df], axis=1)
            return summary_df

        # Otherwise, return the full multivariate summary as before
        summary_data = {"date": output_dates}
        for stat in ["mean", "lower", "upper"]:
            for s in range(n_series):
                summary_data[f"{stat}_{series_names[s]}"] = [x[s]
                                                             for x in result[stat]]
        summary_df = pd.DataFrame(summary_data)
        if return_sims:
            # sims: shape (replications, horizon, n_series)
            sims = result["sims"]
            flat = []
            for rep in sims:
                for s in range(n_series):
                    flat.append([h[s] for h in rep])
            sims_df = pd.DataFrame(flat).transpose()
            colnames = []
            for r in range(len(sims)):
                for s in range(n_series):
                    colnames.append(f"sim_{r+1}_{series_names[s]}")
            sims_df.columns = colnames
            sims_df.insert(0, "date", output_dates)
            return sims_df
        return summary_df
