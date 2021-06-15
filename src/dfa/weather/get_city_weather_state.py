import src.dfa as dfa
from src.intent.intent import Intent, Command


class GetCityWeatherState(dfa.AbstractState):
    def __init__(self):
        super().__init__()
        self._command_handler[Command.WEATHER] = self.handle_weather_command

    @property
    def is_technical_state(self) -> bool:
        return True

    def handle_weather_command(self, intent: Intent) -> dfa.MoveResponse:
        if "city" in intent.parameters:
            return dfa.MoveResponse(dfa.StartState(), "HOT")
        else:
            return dfa.MoveResponse(dfa.AskCityState(), None)
