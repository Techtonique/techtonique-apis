import forecastingapi as fapi

if __name__ == "__main__":
    ## create an account
    # res_create_account = fapi.create_account(username="tester_py3@example.com", 
    #                                         password="python222orpython333")
    # print(res_create_account)

    ## get a token 
    token = fapi.get_token(username="tester_py3@example.com", password="python222orpython333")
    print(token)

    ## get forecast with prediction interval
    path_to_file = '/Users/t/Documents/datasets/time_series/univariate/nile.csv'
     
    res_get_forecast = fapi.get_forecast(file=path_to_file, 
    token=token)

    print(res_get_forecast)

    res_get_forecast2 = fapi.get_forecast(file=path_to_file, 
    token=token, start_training = 2, n_training = 7, h = 4, level = 90)

    print(res_get_forecast2)

    res_get_forecast3 = fapi.get_forecast(file=path_to_file, 
    token=token, date_formatting="ms",
    start_training = 2, n_training = 7, h = 4, level = 90)

    print(res_get_forecast3)