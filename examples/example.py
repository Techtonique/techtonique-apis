from techtonique_apis import TechtoniqueAPI

api = TechtoniqueAPI()


# Example 1: Forecasting
forecast_result = api.forecasting(
    file_path="/Users/t/Documents/datasets/time_series/univariate/a10.csv",
    base_model="RidgeCV",
    n_hidden_features=5,
    lags=25,
    type_pi="kde",
    replications=10,
    h=5
)
print("Forecasting result:", forecast_result)


# Example 2: Machine Learning Regression
regression_result = api.mlregression(
    file_path="/Users/t/Documents/datasets/tabular/regression/mtcars2.csv",
    base_model="ElasticNet",
    n_hidden_features=5,
    return_pi=True
)
print("Regression result:", regression_result)


# Example 3: GBDT Classification
gbdt_classification_result = api.gbdt_classification(
    file_path="/Users/t/Documents/datasets/tabular/classification/iris_dataset2.csv",
    model_type="lightgbm"
)
print("GBDT Classification result:", gbdt_classification_result)


# Example 4: Reserving
reserving_result = api.reserving(
    file_path="/Users/t/Documents/datasets/tabular/triangle/raa.csv",
    method="chainladder"
)
print("Reserving result:", reserving_result)


# Example 5: Survival Analysis
survival_result = api.survival_curve(
    file_path="/Users/t/Documents/datasets/tabular/survival/kidney.csv",
    method="km",
    patient_id=123
)
print("Survival curve result:", survival_result)


# Example 6: Scenarios
scenarios_result = api.simulate_scenario(
    model="GBM",
    n=10,
    frequency="quarterly",
    x0=100,
    horizon=5,
    theta1=0,
    theta2=0.5,
    theta3=0.5,
)
print("Scenarios result:", scenarios_result)