from telegram import Update
from telegram.ext import CallbackContext, Handler, MessageHandler, Filters

from src.handlers.abstract_handler import AbstractHandler


class MainMessageHandler(AbstractHandler):
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
        callback_context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

    def create(self) -> Handler:
        return MessageHandler(Filters.text & (~Filters.command), self._callback_wrapper)
