import tempfile
import pandas as pd
from xlwings import func, arg, ret
from .techtonique_apis import TechtoniqueAPI

api = TechtoniqueAPI()


@func
@arg("df", index=False, doc="Excel range with columns for survival data.")
@arg("method", doc='Survival analysis method (default: "km")')
@arg("patient_id", doc="(For machine learning 'method's) Patient ID for individual survival curve")
@ret(index=False, doc="Survival curve results as a table for Excel")
def techto_survival(
    df: pd.DataFrame,
    method: str = "km",
    patient_id: int = None,
) -> pd.DataFrame:
    """
    Survival analysis: pass a survival dataset as a DataFrame from Excel, return survival curve.

    Excel/xlwings custom function: Survival analysis on a table from Excel using the Techtonique API.

    Parameters
    ----------

    df : pd.DataFrame
        The input survival data as a DataFrame (from Excel range).

    method : str, default "km"
        Survival analysis method to use.

    patient_id : int, optional
        For machine learning methods, patient ID for individual survival curve.

    Returns
    -------

    pd.DataFrame
        Survival curve results as a DataFrame for Excel.

    ---
    xlwings lite docstring (for Excel help):
    Survival analysis on a table from Excel using the Techtonique API.
    - df: Excel range with columns for survival data.
    - method: Survival analysis method (default: km).
    - patient_id: (For machine learning methods) Patient ID for individual survival curve.
    Returns: Survival curve results as a table for Excel.
    """
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        df.to_csv(tmp.name, index=False)
        result = api.survival_curve(
            file_path=tmp.name,
            method=method,
            patient_id=patient_id,
        )
    return pd.DataFrame(result)
