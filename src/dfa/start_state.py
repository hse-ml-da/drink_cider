import src.dfa as dfa
from src.intent.intent import Intent, Command


class StartState(dfa.AbstractState):
    def __init__(self):
        super().__init__()
        self._command_handler[Command.WEATHER] = self.handle_weather_command

    def handle_weather_command(self, intent: Intent) -> dfa.MoveResponse:
        return dfa.MoveResponse(dfa.GetCityWeatherState(), None)
