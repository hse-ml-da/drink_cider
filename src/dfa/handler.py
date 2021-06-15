from logging import getLogger
from typing import Dict

from src.dfa.abstract_state import AbstractState
from src.dfa.start_state import StartState


class DfaUserHandler:
    def __init__(self):
        self.__logger = getLogger(__file__)
        self.__dfa: Dict[int, AbstractState] = {}

    def get_user_dfa(self, user_id: int) -> AbstractState:
        if user_id not in self.__dfa:
            self.__dfa[user_id] = StartState()
        return self.__dfa[user_id]

    def set_user_dfa(self, user_id: int, state: AbstractState):
        if user_id not in self.__dfa:
            self.__logger.error(f"Can't set new state for {user_id}")
            return
        self.__dfa[user_id] = state

    def clean(self):
        self.__logger.info(f"Clean dfa states")
        self.__dfa: Dict[int, AbstractState] = {}

    def reset_user(self, user_id: int):
        if user_id not in self.__dfa:
            self.__logger.error(f"Try to reset unknown user")
            return
        del self.__dfa[user_id]
