import json

import requests

from accuweather import Accuweather
from properties import Properties
from utils import date_utils, validation_utils

properties = Properties()
accuweather = Accuweather()

storage_api_url = properties.get_value("storage_api", "url")


def get_weather_data(data, initial_date, get_forecast):
    if get_forecast and date_utils.is_date_within_limit(initial_date, accuweather.get_max_forecast_days()):
        weather_data = accuweather.get_weather_data_given_coordinates(data["latitude"], data["longitude"])
        return {
            "forecast": weather_data["forecast"],
            "location_key": weather_data["location_key"]
        }

    if "forecast" in data:
        return {
            "forecast": data["forecast"],
            "location_key": data["location_key"]
        }

    return {
        "forecast": "Not available",
        "location_key": accuweather.get_location_key(data["latitude"], data["longitude"])
    }


def build_body(data, get_forecast=True):
    raw_initial_date = data["initial_date"]
    raw_final_date = data["final_date"]

    initial_date = date_utils.format_date(raw_initial_date)
    final_date = date_utils.format_date(raw_final_date)

    validation_utils.check_date_interval(initial_date, final_date)

    weather_data = get_weather_data(data, initial_date, get_forecast)

    body = {
        "name": data["name"],
        "latitude": float(data["latitude"]),
        "longitude": float(data["longitude"]),
        "initial_date": raw_initial_date,
        "final_date": raw_final_date,
        "location_key": int(weather_data["location_key"]),
        "forecast": weather_data["forecast"]
    }

    return body


def save(data):
    body = build_body(data)
    headers = {"Content-Type": "application/json"}
    response = requests.post(storage_api_url, data=json.dumps(body), headers=headers)
    return json.loads(response.text)["response"]["result"]


def get_by_id_raw(id):
    full_url = f"{storage_api_url}/{id}"
    return requests.get(full_url)

def get_by_id(id):
    response = get_by_id_raw(id)
    return json.loads(response.text)["response"]["result"]


def get_by_coordinates(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon
    }
    response = requests.get(storage_api_url, params=params)
    return json.loads(response.text)["response"]["result"]


def update(id, data, params=None):
    response = get_by_id_raw(id)

    if response.status_code != 200:
        raise Exception("Error when searching event ID: " + response.text)

    current_body = json.loads(response.text)["response"]["result"]

    for key, value in data.items():
        if value is not None:
            current_body[key] = value

    if params is not None and "update_forecast" in params:
        update_forecast = params["update_forecast"]
    else:
        update_forecast = False

    body = build_body(current_body, update_forecast)
    full_url = f"{storage_api_url}/{id}"
    headers = {"Content-Type": "application/json"}

    response = requests.put(full_url, data=json.dumps(body), headers=headers)
    formatted_response = json.loads(response.text)["response"]["result"]

    if response.status_code != 200:
        raise Exception("Error when updating event ID: " + formatted_response)

    return formatted_response


def delete(id):
    full_url = f"{storage_api_url}/{id}"
    response = requests.delete(full_url)
    formatted_response = json.loads(response.text)["response"]["result"]

    if response.status_code != 200:
        raise Exception("Error when deleting event ID: " + formatted_response)

    return formatted_response



