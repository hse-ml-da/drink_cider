from telegram import Update
from telegram.ext import CallbackContext, Handler, MessageHandler, Filters

from src.handlers.abstract_handler import AbstractHandler
from src.model import Model


class MainMessageHandler(AbstractHandler):
    def __init__(self):
        super().__init__()
        self.__model = Model()

    @property
    def command_name(self) -> str:
        return "message"

    def _callback(self, update: Update, callback_context: CallbackContext):
        if update.effective_chat is None:
            self.__logger.error(f"Can't find source chat for {self.command_name} query")
            return
        if update.message is None:
            self.__logger.error(f"Can't find message for {self.command_name} query")
            return
        response_message = self.__model.handle_message(update.effective_chat.id, update.message.text)
        callback_context.bot.send_message(chat_id=update.effective_chat.id, text=response_message)

    def create(self) -> Handler:
        return MessageHandler(Filters.text & (~Filters.command), self._callback_wrapper)
