from abc import ABC
from typing import Dict, Optional

from natasha import Doc


class CommandParser(ABC):
    def process(self, message: Doc) -> Optional[Dict[str, str]]:
        raise NotImplementedError()
