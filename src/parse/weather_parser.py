from typing import Dict

from natasha import Doc

from src.parse.command_parser import CommandParser


class WeatherParser(CommandParser):
    __keywords = ["погода", "температура"]

    def validate_query(self, message: Doc) -> bool:
        ask_for_weather = any([token.lemma in self.__keywords for token in message.tokens])
        specify_location = any([span.type == "LOC" for span in message.spans])
        return ask_for_weather or specify_location

    def extract_parameters(self, message: Doc) -> Dict[str, str]:
        parameters = {}
        for span in message.spans:
            if span.type == "LOC":
                parameters["city"] = span.normal
        return parameters
