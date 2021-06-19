from src import dfa
from src.api.dialogue import Dialogue
from src.parse.intent import Intent


class DialogueState(dfa.BaseState):
    def __init__(self):
        super(DialogueState, self).__init__()
        self.__dialogue_api = Dialogue()

    @property
    def is_technical_state(self) -> bool:
        return True

    def move(self, intent: Intent) -> dfa.MoveResponse:
        answer = self.__dialogue_api.generate_answer(intent.message)
        return dfa.MoveResponse(dfa.StartState(), answer)
