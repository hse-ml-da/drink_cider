from typing import Dict, Optional

from natasha import Doc

from src.parse.command_parsers.command_parser import CommandParser


class CiderParser(CommandParser):
    __keywords = ["сидр", "пиво", "выпить", "напиток", "cider"]

    def process(self, message: Doc) -> Optional[Dict[str, str]]:
        is_keywords = any([t.lemma in self.__keywords for t in message.tokens])
        return {} if is_keywords else None
