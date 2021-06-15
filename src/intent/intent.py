from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict


class Command(Enum):
    WEATHER = auto()
    UNKNOWN = auto()


@dataclass
class Intent:
    command: Command
    message: str
    parameters: Dict[str, str] = field(default_factory=dict)
