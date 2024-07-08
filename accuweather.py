import json

import requests
from properties import Properties


class Accuweather:
    __properties = Properties()
    __section = "accuweather_api"
    __max_forecast_days = 5

    def __init__(self):
        self.__api_key = self.__properties.get_value(self.__section, "key")

    def get_location_data(self, lat, long):
        url = self.__properties.get_value(self.__section, "location_api")
        params = {
            "apikey": self.__api_key,
            "q": f"{lat},{long}"
        }

        try:
            return requests.get(url, params=params)
        except Exception as ex:
            raise Exception("Error when getting location data: " + ex.__str__())

    def get_location_key(self, lat, long):
        location_response = self.get_location_data(lat, long)

        if location_response.status_code == 200:
            location_data = json.loads(location_response.text)
            return location_data["Key"]

        return None

    def get_forecast_given_location_key(self, location_key):
        url = self.__properties.get_value(self.__section, "forecast_api")
        full_url = f"{url}/{location_key}"

        params = {
            "apikey": self.__api_key
        }

        try:
            forecast_response = requests.get(full_url, params=params)

            if forecast_response.status_code == 200:
                forecast_data = json.loads(forecast_response.text)
                return forecast_data["Headline"]["Text"]

        except Exception as ex:
            raise Exception("Error when getting forecast given location key: " + ex.__str__())

        return None

    def get_forecast_given_coordinates(self, lat, long):
        location_key = self.get_location_key(lat, long)

        if location_key is not None:
            return self.get_forecast_given_location_key(location_key)

        return None

    def get_max_forecast_days(self):
        return self.__max_forecast_days
