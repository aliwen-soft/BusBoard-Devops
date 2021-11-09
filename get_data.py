from requests import get
import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")
app_id = os.getenv("APP_ID")

base_api = "https://transportapi.com/v3"

auth_params = {
    "app_id":app_id,
    "api_key":api_key
}


def get_bus_stop_names_and_atco_code(latitude, longitude):
    path = f'{base_api}/uk/places.json?lat={latitude}&lon={longitude}&type=bus_stop'
    json = requests.get(path, params=auth_params).json()["member"]

    stops = []
    for i in range(10):
        stop_data = json[i]
        stops.append((stop_data["name"], stop_data["atcocode"]))

    return stops


def get_bus_stop_data(atcocode):
    path = f'{base_api}/uk/bus/stop/{atcocode}/live.json'

    params = auth_params.copy()
    params["group"] = "route"
    params["nextbuses"] = "yes"
    
    data = requests.get(path, params=params)
    if data.status_code == 200:
        return data.json()["departures"]
    raise ValueError(f"Something has gone wrong getting bus stop {atcocode}")


def parse_bus_stop_data(departures_info):
    buses = []
    for line, bus_info in departures_info.items():
        first_bus = bus_info[0]
        buses.append({"line": line, "direction": first_bus["direction"], "expected_departure_time": first_bus["expected_departure_time"]})
    return buses


def get_lat_and_long(postcode):
    json = requests.get(f"https://api.postcodes.io/postcodes/{postcode}").json()["result"]
    return json["latitude"], json["longitude"]


def get_bus_stop_data_for_postcode(postcode):
    latitude, longitude = get_lat_and_long(postcode)
    return {
        name: parse_bus_stop_data(get_bus_stop_data(atco_code))
        for name, atco_code in get_bus_stop_names_and_atco_code(latitude, longitude)
    }
