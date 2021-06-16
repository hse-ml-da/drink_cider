from telegram import Update
from telegram.ext import CallbackContext

from src.handlers.abstract_handler import AbstractHandler
from src.model import Model


class ResetHandler(AbstractHandler):
    def __init__(self, model: Model):
        super().__init__()
        self.__model = model

    __reset_message = "Хорошо, давай начнём сначала…"

    @property
    def command_name(self):
        return "reset"

    def _callback(self, update: Update, callback_context: CallbackContext):
        if update.effective_chat is None:
            self.__logger.error(f"Can't find source chat for {self.command_name} query")
            return
        self.__model.reset_user(update.effective_chat.id)
        callback_context.bot.send_message(chat_id=update.effective_chat.id, text=self.__reset_message)
