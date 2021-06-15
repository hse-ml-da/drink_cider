from telegram import Update
from telegram.ext import CallbackContext

from src.handlers.abstract_handler import AbstractHandler
from src.model import Model


class GetStateHandler(AbstractHandler):
    def __init__(self, model: Model):
        super().__init__()
        self.__model = model

    __current_state_message = "Your current state in DFA is: "

    @property
    def command_name(self):
        return "state"

    def _callback(self, update: Update, callback_context: CallbackContext):
        if update.effective_chat is None:
            self.__logger.error(f"Can't find source chat for {self.command_name} query")
            return
        current_state = self.__model.get_state(update.effective_chat.id)
        callback_context.bot.send_message(
            chat_id=update.effective_chat.id, text=self.__current_state_message + current_state
        )
