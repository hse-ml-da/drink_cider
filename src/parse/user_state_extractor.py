from typing import Optional

from natasha import Doc
from yargy import or_, rule, Parser
from yargy.predicates import normalized, in_caseless
from yargy.rule import InterpretationRule

from src.parse.intent import UserState


class UserStateExtractor:
    __greetings_keywords = ["привет", "здравствуйте", "дарова", "приветули", "здарова"]
    __day_keywords = ["утро", "день", "вечер", "ночи"]
    __leaving_keywords = ["пока", "прощай", "увидимся"]
    __complex_keywords = ["скорого", "свидания", "завтра"]

    def __init__(self):
        self.__yargi_greeting_parser = Parser(self.__build_greeting_parser_rule())
        self.__yargi_leaving_parser = Parser(self.__build_leaving_parser_rule())

    def get_user_state(self, message: Doc) -> Optional[UserState]:
        if self.__yargi_greeting_parser.find(message.text) is not None:
            return UserState.GREETINGS
        if self.__yargi_leaving_parser.find(message.text) is not None:
            return UserState.LEAVING
        return None

    def __build_greeting_parser_rule(self) -> InterpretationRule:
        simple_greeting = rule(in_caseless(self.__greetings_keywords))
        day_rule = rule(in_caseless(self.__day_keywords))
        complex_greeting = rule(normalized("добрый"), or_(day_rule))
        greeting = or_(simple_greeting, complex_greeting)
        return greeting

    def __build_leaving_parser_rule(self) -> InterpretationRule:
        simple_leaving = rule(in_caseless(self.__leaving_keywords))
        part_complex_leaving = rule(in_caseless(self.__complex_keywords))
        complex_leaving = rule(normalized("до"), or_(part_complex_leaving))
        leaving = or_(simple_leaving, complex_leaving)
        return leaving
