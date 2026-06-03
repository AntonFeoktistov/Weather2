import requests
from django.conf import settings

from weather.dtos import LocationDto, WeatherDto, to_dto
from weather.errors import LocationNotFoundError, WeatherNotFoundError


class WeatherFinder:
    def get_weather_by_location_name(self, location_name):
        try:
            location = self._get_location_by_name(location_name)
            weather = self._get_weather_by_location(location)
            return weather
        except (LocationNotFoundError, WeatherNotFoundError):
            raise WeatherNotFoundError()

    def _get_location_by_name(self, location_name):
        print(location_name)
        print(settings.OPENWEATHER_API_KEY, settings.OPENWEATHER_LOCATION_URL)
        try:
            print(location_name)
            params = {
                "q": location_name,
                "limit": 1,
                "appid": settings.OPENWEATHER_API_KEY,
            }
            response = requests.get(
                settings.OPENWEATHER_LOCATION_URL, params=params, timeout=10
            )
            response.raise_for_status()
            location = response.json()[0]
            print(location)
            location_dto = self._make_location_dto(location)
            return location_dto
        except Exception:
            raise LocationNotFoundError()

    def _get_weather_by_location(self, location: LocationDto):
        try:
            params = {
                "lat": location.lat,
                "lon": location.lon,
                "appid": settings.OPENWEATHER_API_KEY,
                "units": "metric",
                "lang": "ru",
            }
            response = requests.get(
                settings.OPENWEATHER_WEATHER_URL, params=params, timeout=10
            )
            data = response.json()

            if data.get("cod") != 200:
                raise WeatherNotFoundError("OPENWEATHER API Problem")

            weather_dto = self._make_weather_dto(location, data)
            return weather_dto

        except Exception:
            raise WeatherNotFoundError()

    def _make_location_dto(self, location: dict):
        local_names = location.get("local_names", {})
        name_ru = local_names.get("ru", location.get("name"))
        location_dict = {
            "lat": round(location["lat"], 3),
            "lon": round(location["lon"], 3),
            "name_en": location["name"],
            "name_ru": name_ru,
        }
        print(location_dict)
        location_dto = to_dto(LocationDto, location_dict)
        return location_dto

    def _make_weather_dto(self, location: LocationDto, data: dict):
        weather_dict = {
            "location": location,
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
        }
        weather_dto = to_dto(WeatherDto, weather_dict)
        return weather_dto
