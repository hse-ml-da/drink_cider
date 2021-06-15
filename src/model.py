from logging import getLogger

from src.dfa.handler import DfaUserHandler
from src.intent.parser import parse


class Model:
    def __init__(self):
        self.__logger = getLogger(__file__)
        self.__dfa_user_handler = DfaUserHandler()

    def handle_message(self, user_id: int, message: str) -> str:
        intent = parse(message)
        current_state = self.__dfa_user_handler.get_user_dfa(user_id)
        response = current_state.move(intent)
        self.__dfa_user_handler.set_user_dfa(user_id, response.new_state)
        return response.response
