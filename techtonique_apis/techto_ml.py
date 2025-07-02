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
    Run sklearn-style classification on a table from Excel using the Techtonique API.
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
    Run regression on a table from Excel using the Techtonique API.
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
        return(pd.DataFrame({
            "prediction": result["y_pred"],
            "lower": result["pi_lower"],
            "upper": result["pi_upper"],
        }))
    return(pd.DataFrame({
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
    Run GBDT regression on a table from Excel using the Techtonique API.
    """
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        df.to_csv(tmp.name, index=False)
        result = api.gbdt_regression(
            file_path=tmp.name,
            model_type=model_type,
        )
    if return_pi:
        return(pd.DataFrame({
            "prediction": result["y_pred"],
            "lower": result["pi_lower"],
            "upper": result["pi_upper"],
        }))
    return(pd.DataFrame({
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
    Run GBDT classification on a table from Excel using the Techtonique API.
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




