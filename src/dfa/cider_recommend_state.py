from typing import Optional

from src import dfa
from src.api.cider_adviser import CiderAdviser
from src.dfa import StartState
from src.parse.intent import Intent


class CiderRecommendState(dfa.BaseState):
    __cider_message = """
Как насчёт:

*{}*
пивоварня: {}
стиль: {}
abv: {}%
rating: {}/5

Более подробно про него можно посмотреть на [untappd]({}).
"""
    _disable_message = "Я сейчас на дегустациях, вернусь позже и расскажу что лучше всего брать!"

    def __init__(self):
        super().__init__()
        self.__cider_advisor = CiderAdviser()
        if not self.__cider_advisor.enabled:
            self.move = self._disable_move

    @property
    def introduce_message(self) -> Optional[str]:
        return "Какой сидр ты хочешь выпить?"

    def move(self, intent: Intent, user_id: int) -> dfa.MoveResponse:
        cider = self.__cider_advisor.get_advise(intent.message)
        message = self.__cider_message.format(
            cider.name, cider.brewery, cider.style, cider.abv, cider.rating, cider.url
        ).strip()
        return dfa.MoveResponse(StartState(), message)
