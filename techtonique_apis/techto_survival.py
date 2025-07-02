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
    Run survival analysis on a table from Excel using the Techtonique API.
    """
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        df.to_csv(tmp.name, index=False)
        result = api.survival_curve(
            file_path=tmp.name,
            method=method,
            patient_id=patient_id,
        )
    return pd.DataFrame(result)
