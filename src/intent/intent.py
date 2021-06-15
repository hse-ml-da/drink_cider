from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List


class Command(Enum):
    WEATHER = auto()
    UNKNOWN = auto()


@dataclass
class Intent:
    command: Command
    message: str
    parameters: List[str] = field(default_factory=list)
