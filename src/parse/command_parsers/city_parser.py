from typing import Optional, Dict

from natasha import Doc

from src.parse.city_extractor import CityExtractor
from src.parse.command_parsers.command_parser import CommandParser


class CityParser(CommandParser):
    def __init__(self, city_extractor: CityExtractor):
        self.__city_extractor = city_extractor

    def process(self, message: Doc) -> Optional[Dict[str, str]]:
        city = self.__city_extractor.extract_city(message)
        if city is not None:
            return {"city": city}
        return None
