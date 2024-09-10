import forecastingapi as fapi
import pandas as pd 
from time import time

if __name__ == "__main__":
    
    token = input("Enter your token: ")
    
    path_to_file = 'https://raw.githubusercontent.com/Techtonique/datasets/main/time_series/univariate/AirPassengers.csv'
    path_to_file2 = '/Users/t/Documents/datasets/time_series/univariate/a10.csv' 
     
    print("\n Example 1 --------------- \n")
    start = time() 
    res_get_forecast = fapi.get_forecast(file=path_to_file2, 
    token=token, endpoint="forecastingreglinear",
    method="BayesianRidge",
    n_hidden_features=5,
    lags=25,
    type_pi='scp2-kde',
    replications=100,
    h=7)
    print(f"Elapsed: {time() - start} seconds \n")
    
    print(res_get_forecast)
