import forecastingapi as fapi
import pandas as pd 
from time import time

if __name__ == "__main__":
    
    #"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NGY3ZDE3Ny05OWQ0LTQzNDktOTc1OC0zZTBkOGVkYWZkYWUiLCJlbWFpbCI6InRoaWVycnkubW91ZGlraS50ZWNodG9uaXF1ZUBnbWFpbC5jb20iLCJleHAiOjE3MjU5Njk2OTB9.UZQsunVFY1A7kfC4t-zP5nQ1VTi5RPRpjQqNoZqNQ8I"
    token = input("Enter your token: ")
    ## 3 - get forecast with prediction interval (for a file or a url)
    path_to_file = 'https://raw.githubusercontent.com/Techtonique/datasets/main/time_series/univariate/AirPassengers.csv'
    path_to_file2 = '/Users/t/Documents/datasets/time_series/univariate/AirPassengers.csv' 
     
    print("\n Example 1 --------------- \n")
    start = time() 
    res_get_forecast = fapi.get_forecast(file=path_to_file2, 
    token=token, endpoint="forecastinggbdt",
    method="RidgeCV",
    n_hidden_features=5,
    lags=25,
    type_pi='gaussian',
    h=10,
)
    print(f"Elapsed: {time() - start} seconds \n")
    
    print(res_get_forecast)
