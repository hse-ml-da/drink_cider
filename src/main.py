import logging
import os

from src.bot_controller import BotController

TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


if __name__ == "__main__":
    __token = os.environ.get(TELEGRAM_BOT_TOKEN)
    if __token is None:
        print(f'can\'t find token for bot in env variable "{TELEGRAM_BOT_TOKEN}"')
    else:
        __bot_controller = BotController(__token)
        __bot_controller.start()
