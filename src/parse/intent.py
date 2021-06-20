from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, Optional


class Command(Enum):
    WEATHER = auto()
    CITY = auto()
    UNKNOWN = auto()


class UserState(Enum):
    GREETINGS = auto()
    LEAVING = auto()


@dataclass
class Intent:
    command: Command
    message: str
    parameters: Dict[str, str] = field(default_factory=dict, init=True)
    user_state: Optional[UserState] = None
