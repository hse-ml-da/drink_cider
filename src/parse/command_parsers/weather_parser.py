from typing import Dict, Optional

from natasha import Doc

from src.api.weather import WeatherTime
from src.parse.city_extractor import CityExtractor
from src.parse.command_parsers.command_parser import CommandParser


class WeatherParser(CommandParser):
    __keywords = ["погода", "температура", "прогноз"]
    __tomorrow_keywords = ["завтра"]
    __week_keywords = ["неделя"]

    def __init__(self, city_extractor: CityExtractor):
        self.__city_extractor = city_extractor
        self.__time_keywords = {WeatherTime.TOMORROW: self.__tomorrow_keywords, WeatherTime.WEEK: self.__week_keywords}

    def process(self, message: Doc) -> Optional[Dict[str, str]]:
        is_keywords = any([t.lemma in self.__keywords for t in message.tokens])
        if not is_keywords:
            return None
        params = {}
        city = self.__city_extractor.extract_city(message)
        if city is not None:
            params["city"] = city
        params["time"] = WeatherTime.TODAY
        for time, keywords in self.__time_keywords.items():
            if any([t.lemma in keywords for t in message.tokens]):
                params["time"] = time
        return params
