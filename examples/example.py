import forecastingapi as fapi
import pandas as pd 
from time import time

if __name__ == "__main__":
    
    ## 1 - create an account (once)
    #res_create_account = fapi.create_account(username="user20231122@example.com", 
    #                                         password="pwd") # choose a better password
    #print(res_create_account)

    # 2 - get a token 
    token = fapi.get_token(username = "user20231122@example.com",
                                   password = "pwd") # choose a better password

    ## 3 - get forecast with prediction interval (for a file or a url)
    path_to_file = 'https://raw.githubusercontent.com/Techtonique/datasets/main/time_series/univariate/AirPassengers.csv'
    path_to_file2 = './datasets/AirPassengers.csv' 
     
    print("\n Example 1 --------------- \n")
    start = time() 
    res_get_forecast = fapi.get_forecast(file=path_to_file, 
    token=token, method = "theta")
    print(f"Elapsed: {time() - start} seconds \n")

    print(f"mean forecast: \n {pd.DataFrame(res_get_forecast['averages'], columns=['date', 'mean'])}\n")
    print(f"prediction intervals: \n {pd.DataFrame(res_get_forecast['ranges'], columns=['date', 'lower', 'upper'])}")

    print("\n Example 2 --------------- \n")
    start = time()
    res_get_forecast2 = fapi.get_forecast(file=path_to_file2, 
    token=token, start_training = 2, n_training = 7, h = 10, level = 90)
    print(f"Elapsed: {time() - start} seconds")

    print(f"mean forecast: \n {pd.DataFrame(res_get_forecast2['averages'], columns=['date', 'mean'])}\n")
    print(f"prediction intervals: \n {pd.DataFrame(res_get_forecast2['ranges'], columns=['date', 'lower', 'upper'])}")

    print("\n Example 3 --------------- \n")
    start = time()
    res_get_forecast3 = fapi.get_forecast(file=path_to_file, 
    token=token, date_formatting="ms",
    start_training = 2, n_training = 7, h = 10, level = 90)
    print(f"Elapsed: {time() - start} seconds")

    print(f"mean forecast: \n {pd.DataFrame(res_get_forecast3['averages'], columns=['date', 'mean'])}\n")
    print(f"prediction intervals: \n {pd.DataFrame(res_get_forecast3['ranges'], columns=['date', 'lower', 'upper'])}")

    print("\n Example 4 --------------- \n")
    start = time()
    res_get_forecast4 = fapi.get_forecast(file=path_to_file2, 
    token=token, method = "prophet", h=10)
    print(f"Elapsed: {time() - start} seconds \n")

    print(f"mean forecast: \n {pd.DataFrame(res_get_forecast4['averages'], columns=['date', 'mean'])}\n")
    print(f"prediction intervals: \n {pd.DataFrame(res_get_forecast4['ranges'], columns=['date', 'lower', 'upper'])}")