from typing import Dict, Optional

from natasha import Doc

from src.parse.ciry_extractor import CityExtractor
from src.parse.command_parsers.command_parser import CommandParser


class WeatherParser(CommandParser):
    def __init__(self, city_extractor: CityExtractor):
        self.__city_extractor = city_extractor

    __keywords = ["погода", "температура", "прогноз"]

    def process(self, message: Doc) -> Optional[Dict[str, str]]:
        is_keywords = any([t.lemma in self.__keywords for t in message.tokens])
        if not is_keywords:
            return None
        city = self.__city_extractor.extract_city(message)
        if city is not None:
            return {"city": city}
        return {}
