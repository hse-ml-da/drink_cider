from telegram import Update
from telegram.ext import CallbackContext

from src.handlers.abstract_handler import AbstractHandler


class HelpHandler(AbstractHandler):

    __help_message = (
        "Сейчас я умею:\n"
        '1. Рекомендовать сидр. Попроси помочь с выбором сидра, например, "Подскажи сидр", и следуй инструкциям.\n'
        "2. Подсказать погоду в городе. Попроси рассказать про погоду, город можешь сразу указать или позже.\n"
        "3. Просто поболтать. Напиши что-нибудь на любую тему и я отвечу.\n"
        "Если я потерялся и не могу тебя понять, то команда /reset вернёт нас в самое начало."
    )

    @property
    def command_name(self):
        return "help"

    def _callback(self, update: Update, callback_context: CallbackContext):
        if update.effective_chat is None:
            self.__logger.error(f"Can't find source chat for {self.command_name} query")
            return
        callback_context.bot.send_message(chat_id=update.effective_chat.id, text=self.__help_message)
