from telegram import Update
from telegram.ext import CallbackContext

from src.handlers.abstract_handler import AbstractHandler


class StartHandler(AbstractHandler):

    __start_message = (
        "Hi! I'm a nice bot that can help with cider! "
        "Just ask me what you want in free form. Also, I can talk about weather in some city."
    )

    @property
    def command_name(self):
        return "start"

    def _callback(self, update: Update, callback_context: CallbackContext):
        if update.effective_chat is None:
            self.__logger.error(f"Can't find source chat for {self.command_name} query")
            return
        callback_context.bot.send_message(chat_id=update.effective_chat.id, text=self.__start_message)
