from typing import Optional

import src.dfa as dfa
from src.parse.intent import Intent, Command


class AskCityState(dfa.BaseState):
    def __init__(self):
        super().__init__()
        self._command_handler[Command.WEATHER] = self.handle_weather_command

    @property
    def introduce_message(self) -> Optional[str]:
        return "Какой город тебя интересует?"

    def handle_weather_command(self, intent: Intent) -> dfa.MoveResponse:
        if "city" in intent.parameters:
            return dfa.MoveResponse(dfa.GetCityWeatherState(), None)
        return self.handle_unknown_command()
