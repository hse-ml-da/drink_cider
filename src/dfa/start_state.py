from src.dfa.abstract_state import AbstractState, MoveResponse
from src.intent.intent import Intent, Command


class StartState(AbstractState):
    def __init__(self):
        super().__init__()
        self._command_handler[Command.WEATHER] = self.handle_weather_command

    def handle_weather_command(self, intent: Intent) -> MoveResponse:
        return MoveResponse(self, "It works!")
