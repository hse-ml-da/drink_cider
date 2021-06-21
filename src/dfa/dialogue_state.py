from src import dfa
from src.api.dialogue import Dialogue
from src.parse.intent import Intent


class DialogueState(dfa.BaseState):
    __disable_message = "Я сейчас не в настроении вести беседу."

    def __init__(self):
        super(DialogueState, self).__init__()
        self.__dialogue_api = Dialogue()
        if not self.__dialogue_api.enabled:
            self.move = self.__disable_move

    @property
    def is_technical_state(self) -> bool:
        return True

    def __disable_move(self, intent: Intent) -> dfa.MoveResponse:
        return dfa.MoveResponse(dfa.StartState(), self.__disable_message)

    def move(self, intent: Intent) -> dfa.MoveResponse:
        answer = self.__dialogue_api.generate_answer(intent.message)
        return dfa.MoveResponse(dfa.StartState(), answer)
