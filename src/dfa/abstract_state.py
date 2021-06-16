from abc import ABC
from dataclasses import dataclass
from typing import Dict, Callable, Optional

from src.parse.intent import Intent, Command


@dataclass
class MoveResponse:
    new_state: "AbstractState"
    message: Optional[str]


IntentHandler = Callable[[Intent], MoveResponse]


class AbstractState(ABC):
    def __init__(self):
        self._command_handler: Dict[Command, IntentHandler] = {}

    @property
    def introduce_message(self) -> Optional[str]:
        return None

    @property
    def is_technical_state(self) -> bool:
        return False

    def move(self, intent: Intent) -> MoveResponse:
        if intent.command in self._command_handler:
            return self._command_handler[intent.command](intent)
        return self.handle_unknown_command()

    def handle_unknown_command(self) -> MoveResponse:
        return MoveResponse(self, "Прости, я не понимаю тебя 🙈")
