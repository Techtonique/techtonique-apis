import pandas as pd
from xlwings import func, arg, ret
from .techtonique_apis import TechtoniqueAPI

api = TechtoniqueAPI()


@func
@arg("model", doc='Simulation model (default: "GBM")')
@arg("n", doc="Number of scenarios (default: 10)")
@arg("horizon", doc="Simulation horizon (default: 5)")
@arg("frequency", doc='Frequency (default: "quarterly")')
@arg("x0", doc="Initial value (default: 1.0)")
@arg("theta1", doc="Model parameter theta1 (default: 0.0)")
@arg("theta2", doc="Model parameter theta2 (default: 0.5)")
@arg("theta3", doc="Model parameter theta3 (optional)")
@arg("seed", doc="Random seed (optional)")
@ret(index=False, doc="Simulation results as a table for Excel")
def techto_simulation(
    model: str = "GBM",
    n: int = 10,
    horizon: int = 5,
    frequency: str = "quarterly",
    x0: float = 1.0,
    theta1: float = 0.0,
    theta2: float = 0.5,
    theta3: float = None,
    seed: int = None,
) -> pd.DataFrame:
    """
    Simulation: run scenario simulation using the Techtonique API.

    Excel/xlwings custom function: Run scenario simulation from Excel using the Techtonique API.

    Parameters
    ----------

    model : str, default "GBM"
        Simulation model to use.

    n : int, default 10
        Number of scenarios.

    horizon : int, default 5
        Simulation horizon.

    frequency : str, default "quarterly"
        Frequency of simulation.

    x0 : float, default 1.0
        Initial value.

    theta1 : float, default 0.0
        Model parameter theta1.

    theta2 : float, default 0.5
        Model parameter theta2.

    theta3 : float, optional
        Model parameter theta3.

    seed : int, optional
        Random seed.

    Returns
    -------

    pd.DataFrame
        Simulation results as a DataFrame for Excel.

    ---
    xlwings lite docstring (for Excel help):
    Run scenario simulation from Excel using the Techtonique API.
    - model: Simulation model (default: GBM).
    - n: Number of scenarios (default: 10).
    - horizon: Simulation horizon (default: 5).
    - frequency: Frequency (default: quarterly).
    - x0: Initial value (default: 1.0).
    - theta1: Model parameter theta1 (default: 0.0).
    - theta2: Model parameter theta2 (default: 0.5).
    - theta3: Model parameter theta3 (optional).
    - seed: Random seed (optional).
    Returns: Simulation results as a table for Excel.
    """
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
    # Adjust as needed based on API response structure
    return pd.DataFrame(result["sims"])
