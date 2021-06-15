import logging
import os
from typing import List

from telegram.ext import Updater, Handler

from src.handlers.main_message_handler import MainMessageHandler
from src.handlers.start_handler import StartHandler

TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


class BotController:
    def __init__(self, token: str):
        self.__logger = logging.getLogger(__file__)

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


if __name__ == "__main__":
    __token = os.environ.get(TELEGRAM_BOT_TOKEN)
    if __token is None:
        print(f'can\'t find token for bot in env variable "{TELEGRAM_BOT_TOKEN}"')
    else:
        __bot_controller = BotController(__token)
        __bot_controller.start()
