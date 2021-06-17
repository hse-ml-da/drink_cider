from os.path import join
from typing import Dict, Optional

from natasha import Doc
from natasha.grammars.addr import Settlement, INT, DOT, TITLE, NOUN, ADJF, DASH
from yargy import Parser, or_, rule, and_
from yargy.pipelines import morph_pipeline
from yargy.predicates import in_caseless, caseless, normalized, dictionary
from yargy.rule import InterpretationRule

from src.parse.command_parser import CommandParser


class WeatherParser(CommandParser):
    __keywords = ["погода", "температура"]

    __city_abbreviations = {
        "Москва": ["мск"],
        "Санкт-Петербург": ["спб", "питер", "петербург", "расчленинград"],
        "Новосибирск": ["нск"],
        "Екатеринбург": ["екб"],
    }
    __simple_city_names_file = join("src", "resources", "simple_city_names.txt")
    __complex_city_names_file = join("src", "resources", "complex_city_names.txt")

    def __init__(self):
        yargi_interpolation_rule = self.__rebuild_yargi_parser_rules()
        self.__yargi_parser = Parser(yargi_interpolation_rule)

    def __extract_city(self, message: Doc) -> Optional[str]:
        for span in message.spans:
            if span.type == "LOC":
                return span.normal
        for token in message.tokens:
            if self.__yargi_parser.match(token.lemma) is not None:
                return self.__back_translation(token.lemma)
        return None

    def process(self, message: Doc) -> Optional[Dict[str, str]]:
        city = self.__extract_city(message)
        is_keywords = any([t.lemma in self.__keywords for t in message.tokens])
        if city is not None:
            return {"city": city}
        if is_keywords:
            return {}
        return None

    def __back_translation(self, city: str) -> str:
        for name, abbreviation in self.__city_abbreviations.items():
            if city in abbreviation:
                return name
        return city

    def __rebuild_yargi_parser_rules(self) -> InterpretationRule:
        with open(self.__simple_city_names_file, "r") as f:
            simple_city_names = dictionary([name.strip() for name in f])
        with open(self.__complex_city_names_file, "r") as f:
            complex_city_names = morph_pipeline([name.strip() for name in f])

        city_abbreviations = in_caseless(sum(self.__city_abbreviations.values(), []))
        city_name = or_(rule(simple_city_names), complex_city_names, rule(city_abbreviations)).interpretation(
            Settlement.name
        )

        simple_name = and_(TITLE, or_(NOUN, ADJF))
        complex_name = or_(
            rule(simple_name, DASH.optional(), simple_name),
            rule(TITLE, DASH.optional(), caseless("на"), DASH.optional(), TITLE),
        )
        name = or_(rule(simple_name), complex_name)
        maybe_city_name = or_(name, rule(name, "-", INT)).interpretation(Settlement.name)

        city_words = or_(rule(normalized("город")), rule(caseless("г"), DOT.optional())).interpretation(
            Settlement.type.const("город")
        )
        city = or_(rule(city_words, maybe_city_name), rule(city_words.optional(), city_name)).interpretation(Settlement)
        return city
