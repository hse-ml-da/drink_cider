from dataclasses import dataclass
from logging import getLogger
from typing import Dict, Callable, Optional

from src import dfa
from src.parse.intent import Intent, Command
from src.singleton import Singleton


@dataclass
class MoveResponse:
    new_state: "BaseState"
    message: Optional[str]


IntentHandler = Callable[[Intent, int], MoveResponse]


class BaseState(metaclass=Singleton):
    _disable_message = None

    def __init__(self):
        self._logger = getLogger(__file__)
        self._command_handler: Dict[Command, IntentHandler] = {}

    @property
    def introduce_message(self) -> Optional[str]:
        return None

    @property
    def is_technical_state(self) -> bool:
        return False

    def _disable_move(self, intent: Intent, user_id) -> MoveResponse:
        return MoveResponse(dfa.StartState(), self._disable_message)

    def move(self, intent: Intent, user_id: int) -> MoveResponse:
        if intent.command in self._command_handler:
            return self._command_handler[intent.command](intent, user_id)
        return self.handle_unknown_command()

    def handle_unknown_command(self) -> MoveResponse:
        return MoveResponse(self, "Прости, я не понимаю тебя 🙈")
