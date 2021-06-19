import src.dfa as dfa
from src.dfa.dialogue_state import DialogueState
from src.parse.intent import Intent, Command


class StartState(dfa.BaseState):
    def __init__(self):
        super().__init__()
        self._command_handler[Command.WEATHER] = self.handle_weather_command

    def handle_weather_command(self, intent: Intent) -> dfa.MoveResponse:
        return dfa.MoveResponse(dfa.GetCityWeatherState(), None)

    def handle_unknown_command(self) -> dfa.MoveResponse:
        return dfa.MoveResponse(dfa.DialogueState(), None)
