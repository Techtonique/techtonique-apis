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
    Reserving: pass a triangle as a DataFrame from Excel, return reserving results.

    Excel/xlwings custom function: Classical reserving on a triangle from Excel using the Techtonique API.

    Parameters
    ----------

    df : pd.DataFrame
        The input triangle data as a DataFrame (from Excel range).

    method : str, default "chainladder"
        Reserving method to use.

    Returns
    -------

    pd.DataFrame
        Reserving results as a DataFrame for Excel.

    ---
    xlwings lite docstring (for Excel help):
    Classical reserving on a triangle from Excel using the Techtonique API.
    - df: Excel range with reserving triangle data.
    - method: Reserving method (default: chainladder).
    Returns: Reserving results as a table for Excel.
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
    ML Reserving: pass a triangle as a DataFrame from Excel, return ML reserving results.

    Excel/xlwings custom function: ML reserving on a triangle from Excel using the Techtonique API.

    Parameters
    ----------

    df : pd.DataFrame
        The input triangle data as a DataFrame (from Excel range).

    method : str, default "RidgeCV"
        ML reserving method to use.

    Returns
    -------

    pd.DataFrame
        ML reserving results as a DataFrame for Excel.

    ---
    xlwings lite docstring (for Excel help):
    ML reserving on a triangle from Excel using the Techtonique API.
    - df: Excel range with reserving triangle data.
    - method: ML reserving method (default: RidgeCV).
    Returns: ML reserving results as a table for Excel.
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
