import requests
import numpy as np
from datetime import datetime
from dotenv import load_dotenv
import os
import pytz
import pandas as pd

load_dotenv()

class DataGatheringModule:
    """
    Implements the data gathering module for BOG release decision-making.
    """
    def __init__(self):
        """
        Initialize the data gathering module.
        """
        # API keys and endpoints (example values)
        self.weather_api_key = os.environ["WEATHER_API_KEY"]
        self.weather_api_url = "https://api.openweathermap.org/data/3.0/onecall"
        self.population_data = pd.read_csv("population_density.csv")
        self.google_maps_api_key = os.environ["GOOGLE_MAPS_API_KEY"]

    def get_population_density(self, latitude, longitude):
        """
        Get population density for a given location.
        
        :param latitude: Latitude of the location.
        :param longitude: Longitude of the location.
        :return: Population density (people per square kilometer).
        """
        
        # Compute Euclidean distance between the query point and each row in the dataset
        self.population_data["distance"] = ((self.population_data["Y"] - latitude)**2 + (self.population_data["X"] - longitude)**2)**0.5
        
        # Find the row with the smallest distance
        closest_row = self.population_data.loc[self.population_data["distance"].idxmin()]
        
        return closest_row["Z"]

    def get_road_type_google(self, latitude, longitude):
        """
        Get road type using the Google Maps Geocoding API.
        
        :param latitude: Latitude of the location.
        :param longitude: Longitude of the location.
        :return: List of types associated with the road.
        """
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "latlng": f"{latitude},{longitude}",
            "key": self.google_maps_api_key,
            # You can restrict the result types if needed:
            "result_type": "route"  
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                # The 'types' field gives types, e.g. ["route"] or ["highway"]
                road_types = data["results"][0].get("types", [])
                return road_types
            else:
                raise Exception("No results for the provided coordinates")
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")


    def get_weather_condition(self, latitude, longitude):
        """
        Get the current weather condition for a given location.
        
        :param latitude: Latitude of the location.
        :param longitude: Longitude of the location.
        :return: Weather condition (e.g., "sunny", "rain", "thunderstorm").
        """
        # Example: Fetch weather data from OpenWeatherMap API
        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": self.weather_api_key,
            "units": "metric"
        }
        response = requests.get(self.weather_api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data["weather"][0]["main"].lower()  # Extract weather condition
        else:
            raise Exception(f"Failed to fetch weather data: {response.status_code}")

    def get_driving_time(self):
        """
        Get the current time of day.
        
        :return: Time of day (e.g., "daytime", "nighttime", "rush_hour").
        """
        shanghai_tz = pytz.timezone("Asia/Shanghai")
        now = datetime.now(shanghai_tz)
        hour = now.hour

        if 7 <= hour < 9 or 17 <= hour < 19:
            return "rush_hour"
        elif 6 <= hour < 18:
            return "daytime"
        else:
            return "nighttime"

    def get_site_type_google(self, latitude, longitude):
        """
        Determine the site type using the Google Maps Geocoding API.
        
        :param latitude: Latitude of the location.
        :param longitude: Longitude of the location.
        :return: Inferred site type (e.g., "urban", "rural").
        """
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "latlng": f"{latitude},{longitude}",
            "key": self.google_maps_api_key,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                address_components = data["results"][0].get("address_components", [])
                # You can inspect address_components to decide the site type.
                # For example, if a 'locality' or 'sublocality' is found, you might infer an urban area.
                types = []
                for component in address_components:
                    types.extend(component.get("types", []))
                if "locality" in types or "sublocality" in types:
                    return "urban"
                else:
                    return "rural"
            else:
                raise Exception("No results for the provided coordinates")
        else:
            raise Exception(f"Failed to fetch site type data: {response.status_code}")


# Example Usage of the Data Gathering Module
if __name__ == "__main__":
    # Initialize the data gathering module
    data_gatherer = DataGatheringModule()

    # Example location (latitude and longitude)
    latitude = 34.0522  # Example: Los Angeles
    longitude = -118.2437

    # Gather data
    population_density = data_gatherer.get_population_density(latitude, longitude)
    road_type = data_gatherer.get_road_type(latitude, longitude)
    weather_condition = data_gatherer.get_weather_condition(latitude, longitude)
    driving_time = data_gatherer.get_driving_time()
    site_type = data_gatherer.get_site_type(latitude, longitude)

    # Output gathered data
    print("Gathered Data:")
    print(f"Population Density: {population_density} people/km²")
    print(f"Road Type: {road_type}")
    print(f"Weather Condition: {weather_condition}")
    print(f"Driving Time: {driving_time}")
    print(f"Site Type: {site_type}")