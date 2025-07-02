import tempfile
import pandas as pd
from xlwings import func, arg, ret
from .techtonique_apis import TechtoniqueAPI

api = TechtoniqueAPI()

@func
@arg("df", index=False, doc="Excel range with reserving triangle data.")
@arg("method", doc='Reserving method (default: "chainladder")')
@ret(index=False, doc="Reserving results as a table for Excel")
def techto_reserving(
    df: pd.DataFrame,
    method: str = "chainladder",
) -> pd.DataFrame:
    """
    Run classical reserving on a triangle from Excel using the Techtonique API.
    """
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        df.to_csv(tmp.name, index=False)
        result = api.reserving(
            file_path=tmp.name,
            method=method,
        )
    if method == "chainladder": 
        return pd.DataFrame(result)
    return pd.DataFrame({"origin": result["Origin"], 
                         "IBNR": result["IBNR"], 
                         "IBNR 95": result["IBNR 95%"]})

@func
@arg("df", index=False, doc="Excel range with reserving triangle data.")
@arg("method", doc='ML reserving method (default: "RidgeCV")')
@ret(index=False, doc="ML reserving results as a table for Excel")
def techto_mlreserving(
    df: pd.DataFrame,
    method: str = "RidgeCV",
) -> pd.DataFrame:
    """
    Run ML reserving on a triangle from Excel using the Techtonique API.
    """
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        df.to_csv(tmp.name, index=False)
        result = api.mlreserving(
            file_path=tmp.name,
            method=method,
        )
    return pd.DataFrame({"origin": result["Origin"], 
                         "IBNR": result["IBNR"], 
                         "IBNR 95": result["IBNR 95%"]})