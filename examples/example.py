from techtonique_apis import TechtoniqueAPI

api = TechtoniqueAPI()

# Example 1: Forecasting
forecast_result = api.forecasting(
    file_path="a10.csv",
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
    file_path="mtcars2.csv",
    base_model="ElasticNet",
    n_hidden_features=5,
    return_pi=True
)
print("Regression result:", regression_result)

# Example 4: Reserving
reserving_result = api.mlreserving(
    file_path="raa.csv",
    method="RandomForestRegressor"
)
print("Reserving result:", reserving_result)


# Example 5: Survival Analysis
survival_result = api.survival_curve(
    file_path="kidney.csv",
    method="km",
    patient_id=123
)
print("Survival curve result:", survival_result)


# # Example 6: Scenarios
# scenarios_result = api.simulate_scenario(
#     model="GBM",
#     n=10,
#     frequency="quarterly",
#     x0=100,
#     horizon=5,
#     theta1=0,
#     theta2=0.5,
#     theta3=0.5,
# )
# print("Scenarios result:", scenarios_result)