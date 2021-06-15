from logging import getLogger
from typing import List

from telegram.ext import Updater, Handler

from src.handlers.main_message_handler import MainMessageHandler
from src.handlers.start_handler import StartHandler


class BotController:
    def __init__(self, token: str):
        self.__logger = getLogger(__file__)

        self.__updater = Updater(token)
        self.__dispatcher = self.__updater.dispatcher
        for handler in self.__init_handlers():
            self.__dispatcher.add_handler(handler)

    @staticmethod
    def __init_handlers() -> List[Handler]:
        return [StartHandler().create(), MainMessageHandler().create()]

    def start(self):
        self.__logger.info("Starting bot")
        self.__updater.start_polling()
        self.__updater.idle()
