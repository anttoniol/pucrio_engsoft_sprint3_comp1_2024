import json

import requests

from accuweather import Accuweather
from properties import Properties
from utils import date_utils, validation_utils

properties = Properties()
accuweather = Accuweather()

storage_api_url = properties.get_value("storage_api", "url")


def build_body(data, get_forecast=True):
    initial_date = data["initial_date"]
    final_date = data["final_date"]

    formatted_initial_date = date_utils.format_date(initial_date)
    formatted_final_date = date_utils.format_date(final_date)

    validation_utils.check_date_interval(formatted_initial_date, formatted_final_date)

    if get_forecast and date_utils.is_date_within_limit(formatted_initial_date, accuweather.get_max_forecast_days()):
        forecast = accuweather.get_forecast_given_coordinates(data["latitude"], data["longitude"])
    elif "forecast" in data:
        forecast = data["forecast"]
    else:
        forecast = "Not available"

    body = data.copy()
    body["forecast"] = forecast

    return body


def save(data):
    body = build_body(data)
    return requests.post(storage_api_url, data = body)


def get_by_id(id):
    full_url = f"{storage_api_url}/{id}"
    return requests.get(full_url)


def get_by_coordinates(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon
    }
    return requests.get(storage_api_url, params=params)


def update(id, data, params=None):
    response = get_by_id(id)

    if response.status_code != 200:
        raise Exception("Error when searching event ID: " + response.text)

    current_body = json.loads(response.text)

    for key, value in data.items():
        if value is not None:
            current_body[key] = value

    if params is not None and "update_forecast" in params:
        update_forecast = params["update_forecast"]
    else:
        update_forecast = False

    body = build_body(data, update_forecast)
    full_url = f"{storage_api_url}/{id}"
    return requests.put(full_url, data=body)


def delete(id):
    full_url = f"{storage_api_url}/{id}"
    response = requests.delete(full_url)

    if response.status_code != 200:
        raise Exception("Error when deleting event ID: " + response.text)



