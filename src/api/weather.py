import os
from dataclasses import dataclass
from enum import Enum, auto
from logging import getLogger
from typing import Optional

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
    weather_description: Optional[WeatherDescription] = None


class WeatherAPI:

    __OPEN_WEATHER_API_KEY = "OPEN_WEATHER_API_KEY"
    __api_endpoint = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self):
        self.__logger = getLogger(__file__)
        self.__api_key = os.environ.get(self.__OPEN_WEATHER_API_KEY)
        if self.__api_key is None:
            self.__logger.error(f"Can't find token for open weather API in env var: {self.__OPEN_WEATHER_API_KEY}")

    @property
    def enabled(self) -> bool:
        return self.__api_key is not None

    def __create_request_url(self, city: str) -> str:
        return f"?q={city}&appid={self.__api_key}&lang=ru&units=metric"

    def get_weather(self, city: str) -> Optional[WeatherApiResponse]:
        params = {"q": city, "appid": self.__api_key, "lang": "ru", "units": "metric"}
        response = get(self.__api_endpoint, params=params)
        if response.status_code != 200:
            self.__logger.error(f"Request to open weather return {response.status_code} status code")
            return WeatherApiResponse(ResponseStatus.UNAVAILABLE)
        parsed_response = response.json()
        if parsed_response["cod"] == "404":
            self.__logger.info(f"Request to weather in unknown city: {city}")
            return WeatherApiResponse(ResponseStatus.NOT_FOUND)
        self.__logger.info(f"Successful request for weather in {city}")
        return WeatherApiResponse(
            ResponseStatus.OK,
            WeatherDescription(
                parsed_response["main"]["temp"],
                parsed_response["main"]["feels_like"],
                parsed_response["wind"]["speed"],
                parsed_response["weather"][0]["description"],
            ),
        )
