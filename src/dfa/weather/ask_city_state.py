from typing import Optional

import src.dfa as dfa
from src.intent.intent import Intent, Command


class AskCityState(dfa.AbstractState):
    # def __init__(self):
    #     super().__init__()
    #     self._command_handler[Command.WEATHER] = self.handle_weather_command

    @property
    def introduce_message(self) -> Optional[str]:
        return "Which city are you interested in?"

    # def handle_weather_command(self, intent: Intent) -> MoveResponse:
    #     pass
