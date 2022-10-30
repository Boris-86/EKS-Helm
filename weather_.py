"""
# ===============================================================================
# Python Project - 7 days weather forecast
# Boris Rozenman
# ===============================================================================
"""

# ===============================================================================
#                                 Libraries
# ===============================================================================

import requests
import json

# ===============================================================================
#                                 Constants
# ===============================================================================

deg_sign = u"\N{DEGREE SIGN}"
api_key = "&key=5UNU7BCKU5MGMGA2AEVAETFS8&"
base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
forecast = "/next7days?"
params = "unitGroup=metric&elements=datetime%2Ctempmax%2Ctempmin%2Ctemp%2Chumidity"

# ===============================================================================
#                                 Functions
# ===============================================================================

def __get_api_data(city):
    complete_url = base_url + city + forecast + params + api_key
    response = requests.get(complete_url)
    return response

def __one_day_forecast(response, day):
    day_data = {}
    content = response.content
    print(content)
    day_data["date"] = response["days"][day]["datetime"]
    day_data["temp_night"] = response["days"][day]["tempmin"]
    #day_data["temp_midnight"] = response["days"][day]["hours"][0]["temp"]
    day_data["temp_day"] = response["days"][day]["tempmax"]
    day_data["humidity"] = response["days"][day]["humidity"]
    return day_data


def current_forecast(city):
    fc = __get_api_data(city)
    current_data = {}
    current_data["city"] = fc["address"]
    current_data["full_location"] = fc["resolvedAddress"]
    current_data["time"] = fc["currentConditions"]["datetime"]
    current_data["temp_now"] = fc["currentConditions"]["temp"]
    current_data["humidity_now"] = fc["currentConditions"]["humidity"]
    return current_data


def seven_days_forecast(city):
    fc = __get_api_data(city)
    week_forecast = []
    #week_forecast[0] = get_current_forecast(city)
    for day in range(0, 8):
        week_forecast.append(__one_day_forecast(fc, day))
    return week_forecast

#print(seven_days_forecast("haifa"))
# ===============================================================================
#                                  - MAIN -
# ===============================================================================

city = "telaviv"
week_forecast = seven_days_forecast(city)
today = current_forecast(city)
print(today)
print(week_forecast)

# ===============================================================================
#                                 - END OF FILE -
# ===============================================================================
