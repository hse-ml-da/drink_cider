from typing import Optional

import src.dfa as dfa
from src.parse.intent import Intent, Command


class AskCityState(dfa.BaseState):
    def __init__(self):
        super().__init__()
        self._command_handler[Command.CITY] = self.handle_city_command
        self._command_handler[Command.WEATHER] = self.handle_city_command

    @property
    def introduce_message(self) -> Optional[str]:
        return "Какой город тебя интересует?"

    def handle_city_command(self, intent: Intent) -> dfa.MoveResponse:
        if "city" in intent.parameters:
            intent.command = Command.WEATHER
            return dfa.MoveResponse(dfa.GetCityWeatherState(), None)
        return self.handle_unknown_command()
