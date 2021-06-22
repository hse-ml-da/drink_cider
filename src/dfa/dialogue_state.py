from src import dfa
from src.api.dialogue import Dialogue
from src.parse.intent import Intent


class DialogueState(dfa.BaseState):
    _disable_message = "Я сейчас не в настроении вести беседу."

    def __init__(self):
        super(DialogueState, self).__init__()
        self.__dialogue_api = Dialogue()
        if not self.__dialogue_api.enabled:
            self.move = self._disable_move

    @property
    def is_technical_state(self) -> bool:
        return True

    def move(self, intent: Intent, user_id: int) -> dfa.MoveResponse:
        answer = self.__dialogue_api.generate_answer(intent.message, user_id)
        return dfa.MoveResponse(dfa.StartState(), answer)
