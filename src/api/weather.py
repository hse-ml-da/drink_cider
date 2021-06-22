import os
from dataclasses import dataclass
from enum import Enum, auto
from logging import getLogger
from typing import Optional, Dict, List

from requests import get


@dataclass
class WeatherDescription:
    temperature: float
    feels_like: float
    wind_speed: float
    weather: str


class ResponseStatus(Enum):
    OK = auto()
    UNAVAILABLE = auto()
    NOT_FOUND = auto()


@dataclass
class WeatherApiResponse:
    status: ResponseStatus
    weather_description: Optional[List[WeatherDescription]] = None


class WeatherTime(Enum):
    TODAY = auto()
    TOMORROW = auto()
    WEEK = auto()


class WeatherAPI:

    __OPEN_WEATHER_API_KEY = "OPEN_WEATHER_API_KEY"
    __api_forecast_endpoint = "https://api.openweathermap.org/data/2.5/forecast/daily"
    __api_current_endpoint = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self):
        self.__logger = getLogger(__file__)
        self.__api_key = os.environ.get(self.__OPEN_WEATHER_API_KEY)
        if self.__api_key is None:
            self.__logger.error(f"Can't find token for open weather API in env var: {self.__OPEN_WEATHER_API_KEY}")

    @property
    def enabled(self) -> bool:
        return self.__api_key is not None

    @staticmethod
    def __extract_forecast(raw_weather: Dict) -> List[WeatherDescription]:
        return [
            WeatherDescription(
                response["temp"]["day"],
                response["feels_like"]["day"],
                response["speed"],
                response["weather"][0]["description"],
            )
            for response in raw_weather["list"][1:]
        ]

    @staticmethod
    def __extract_current_weather(raw_weather: Dict) -> WeatherDescription:
        return WeatherDescription(
            raw_weather["main"]["temp"],
            raw_weather["main"]["feels_like"],
            raw_weather["wind"]["speed"],
            raw_weather["weather"][0]["description"],
        )

    def get_weather(self, city: str) -> WeatherApiResponse:
        forecast_params = {"q": city, "appid": self.__api_key, "lang": "ru", "units": "metric", "cnt": 8}
        forecast_response = get(self.__api_forecast_endpoint, params=forecast_params)
        current_params = {"q": city, "appid": self.__api_key, "lang": "ru", "units": "metric"}
        current_response = get(self.__api_current_endpoint, params=current_params)

        for response in [forecast_response, current_response]:
            if response.status_code == 404:
                self.__logger.info(f"Request to weather in unknown city: {city}")
                return WeatherApiResponse(ResponseStatus.NOT_FOUND)
            if response.status_code != 200:
                self.__logger.error(f"Request to open weather return {forecast_response.status_code} status code")
                return WeatherApiResponse(ResponseStatus.UNAVAILABLE)
        self.__logger.info(f"Successful request for weather in {city}")

        forecast_response = self.__extract_forecast(forecast_response.json())
        current_response = self.__extract_current_weather(current_response.json())

        return WeatherApiResponse(ResponseStatus.OK, [current_response] + forecast_response[1:])
