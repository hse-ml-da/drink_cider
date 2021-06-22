import src.dfa as dfa
from src.parse.intent import Intent, Command


class StartState(dfa.BaseState):
    def __init__(self):
        super().__init__()
        self._command_handler[Command.WEATHER] = self.handle_weather_command
        self._command_handler[Command.CIDER] = self.handle_cider_command

    def handle_weather_command(self, intent: Intent, user_id: int) -> dfa.MoveResponse:
        return dfa.MoveResponse(dfa.GetCityWeatherState(), None)

    def handle_cider_command(self, intent: Intent, user_id: int) -> dfa.MoveResponse:
        return dfa.MoveResponse(dfa.CiderRecommendState(), None)

    def handle_unknown_command(self) -> dfa.MoveResponse:
        return dfa.MoveResponse(dfa.DialogueState(), None)
