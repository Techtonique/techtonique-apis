import tempfile
import pandas as pd
from xlwings import func, arg, ret
from .techtonique_apis import TechtoniqueAPI

api = TechtoniqueAPI()


@func
@arg("df", index=False, doc="Excel range with columns for features and target.")
@arg("base_model", doc='Classification model (default: "RandomForestClassifier")')
@arg("n_hidden_features", doc="Number of hidden features (default: 5)")
@arg("predict_proba", doc="If TRUE, return class probabilities (default: FALSE)")
@ret(index=False, doc="Classification predictions as a table for Excel")
def techto_mlclassification(
    df: pd.DataFrame,
    base_model: str = "RandomForestClassifier",
    n_hidden_features: int = 5,
    predict_proba: bool = False,
) -> pd.DataFrame:
    """
    Classification: pass a tabular dataset as a DataFrame from Excel, return predictions.

    Excel/xlwings custom function: Classification on a table from Excel using the Techtonique API.

    Parameters
    ----------

    df : pd.DataFrame
        The input data as a DataFrame (from Excel range).

    base_model : str, default "RandomForestClassifier"
        The classification model to use.

    n_hidden_features : int, default 5
        Number of hidden features for the model.

    predict_proba : bool, default False
        If True, return class probabilities.

    Returns
    -------

    pd.DataFrame
        Classification predictions (and probabilities if requested) as a DataFrame for Excel.

    ---
    xlwings lite docstring (for Excel help):
    Classification on a table from Excel using the Techtonique API.
    - df: Excel range with columns for features and target.
    - base_model: Classification model (default: RandomForestClassifier).
    - n_hidden_features: Number of hidden features (default: 5).
    - predict_proba: If TRUE, return class probabilities (default: FALSE).
    Returns: Classification predictions as a table for Excel.
    """
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        df.to_csv(tmp.name, index=False)
        result = api.mlclassification(
            file_path=tmp.name,
            base_model=base_model,
            n_hidden_features=n_hidden_features,
            predict_proba=predict_proba,
        )
    # Adjust keys as needed based on API response
    if predict_proba and "proba" in result:
        return pd.DataFrame(result["proba"])
    return pd.DataFrame(result["y_pred"])


@func
@arg("df", index=False, doc="Excel range with columns for features and target.")
@arg("base_model", doc='Regression model (default: "ElasticNet")')
@arg("n_hidden_features", doc="Number of hidden features (default: 5)")
@arg("return_pi", doc="If TRUE, return prediction intervals (default: TRUE)")
@ret(index=False, doc="Regression predictions as a table for Excel")
def techto_mlregression(
    df: pd.DataFrame,
    base_model: str = "ElasticNet",
    n_hidden_features: int = 5,
    return_pi: bool = True,
) -> pd.DataFrame:
    """
    Regression: pass a tabular dataset as a DataFrame from Excel, return predictions.

    Excel/xlwings custom function: Regression on a table from Excel using the Techtonique API.

    Parameters
    ----------

    df : pd.DataFrame
        The input data as a DataFrame (from Excel range).

    base_model : str, default "ElasticNet"
        The regression model to use.

    n_hidden_features : int, default 5
        Number of hidden features for the model.

    return_pi : bool, default True
        If True, return prediction intervals.

    Returns
    -------
    pd.DataFrame
        Regression predictions (and intervals if requested) as a DataFrame for Excel.

    ---
    xlwings lite docstring (for Excel help):
    Regression on a table from Excel using the Techtonique API.
    - df: Excel range with columns for features and target.
    - base_model: Regression model (default: ElasticNet).
    - n_hidden_features: Number of hidden features (default: 5).
    - return_pi: If TRUE, return prediction intervals (default: TRUE).
    Returns: Regression predictions as a table for Excel.
    """
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        df.to_csv(tmp.name, index=False)
        result = api.mlregression(
            file_path=tmp.name,
            base_model=base_model,
            n_hidden_features=n_hidden_features,
            return_pi=return_pi,
        )
    if return_pi:
        return (pd.DataFrame({
            "prediction": result["y_pred"],
            "lower": result["pi_lower"],
            "upper": result["pi_upper"],
        }))
    return (pd.DataFrame({
        "prediction": result["y_pred"]
    }))


@func
@arg("df", index=False, doc="Excel range with columns for features and target.")
@arg("model_type", doc='GBDT model type (default: "lightgbm")')
@arg("return_pi", doc="If TRUE, return prediction intervals (default: TRUE)")
@ret(index=False, doc="GBDT regression predictions as a table for Excel")
def techto_gbdt_regression(
    df: pd.DataFrame,
    model_type: str = "lightgbm",
    return_pi: bool = True,
) -> pd.DataFrame:
    """
    GBDT Regression: pass a tabular dataset as a DataFrame from Excel, return predictions.

    Excel/xlwings custom function: GBDT regression on a table from Excel using the Techtonique API.

    Parameters
    ----------

    df : pd.DataFrame
        The input data as a DataFrame (from Excel range).

    model_type : str, default "lightgbm"
        The GBDT model type to use.

    return_pi : bool, default True
        If True, return prediction intervals.

    Returns
    -------

    pd.DataFrame
        GBDT regression predictions (and intervals if requested) as a DataFrame for Excel.

    ---
    xlwings lite docstring (for Excel help):
    GBDT regression on a table from Excel using the Techtonique API.
    - df: Excel range with columns for features and target.
    - model_type: GBDT model type (default: lightgbm).
    - return_pi: If TRUE, return prediction intervals (default: TRUE).
    Returns: GBDT regression predictions as a table for Excel.
    """
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        df.to_csv(tmp.name, index=False)
        result = api.gbdt_regression(
            file_path=tmp.name,
            model_type=model_type,
        )
    if return_pi:
        return (pd.DataFrame({
            "prediction": result["y_pred"],
            "lower": result["pi_lower"],
            "upper": result["pi_upper"],
        }))
    return (pd.DataFrame({
        "prediction": result["y_pred"]
    }))


@func
@arg("df", index=False, doc="Excel range with columns for features and target.")
@arg("model_type", doc='GBDT model type (default: "lightgbm")')
@arg("predict_proba", doc="If TRUE, return class probabilities (default: FALSE)")
@ret(index=False, doc="GBDT classification predictions as a table for Excel")
def techto_gbdt_classification(
    df: pd.DataFrame,
    model_type: str = "lightgbm",
    predict_proba: bool = False,
) -> pd.DataFrame:
    """
    GBDT Classification: pass a tabular dataset as a DataFrame from Excel, return predictions.

    Excel/xlwings custom function: GBDT classification on a table from Excel using the Techtonique API.

    Parameters
    ----------

    df : pd.DataFrame
        The input data as a DataFrame (from Excel range).

    model_type : str, default "lightgbm"
        The GBDT model type to use.

    predict_proba : bool, default False
        If True, return class probabilities.

    Returns
    -------

    pd.DataFrame
        GBDT classification predictions (and probabilities if requested) as a DataFrame for Excel.

    ---
    xlwings lite docstring (for Excel help):
    GBDT classification on a table from Excel using the Techtonique API.
    - df: Excel range with columns for features and target.
    - model_type: GBDT model type (default: lightgbm).
    - predict_proba: If TRUE, return class probabilities (default: FALSE).
    Returns: GBDT classification predictions as a table for Excel.
    """
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        df.to_csv(tmp.name, index=False)
        result = api.gbdt_classification(
            file_path=tmp.name,
            model_type=model_type,
        )
    # Adjust keys as needed based on API response
    if predict_proba and "proba" in result:
        return pd.DataFrame(result["proba"])
    return pd.DataFrame(result["y_pred"])
