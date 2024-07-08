import requests

from accuweather import Accuweather
from properties import Properties
from utils import date_utils, validation_utils

properties = Properties()
accuweather = Accuweather()

storage_api_url = properties.get_value("storage_api", "url")

# sp_coordinates = -23.533773,-46.625290

def save(data):
    initial_date = data["initial_date"]
    final_date = data["final_date"]

    formatted_initial_date = date_utils.format_date(initial_date)
    formatted_final_date = date_utils.format_date(final_date)

    validation_utils.check_date_interval(formatted_initial_date, formatted_final_date)

    if date_utils.is_date_within_limit(formatted_initial_date, accuweather.get_max_forecast_days()):
        forecast = accuweather.get_forecast_given_coordinates(data["latitude"], data["longitude"])
    else:
        forecast = "Not available"

    body = data.copy()
    body["forecast"] = forecast

    return requests.post(storage_api_url, data = body)