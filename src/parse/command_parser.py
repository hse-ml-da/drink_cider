from abc import ABC
from pydoc import Doc
from typing import Dict


class CommandParser(ABC):
    def validate_query(self, message: Doc) -> bool:
        raise NotImplementedError()

    def extract_parameters(self, message: Doc) -> Dict[str, str]:
        raise NotImplementedError()
