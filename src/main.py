import logging
import os

from src.bot_controller import BotController

MODE = "dev"
TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
TELEGRAM_TEST_BOT_TOKEN = "TELEGRAM_TEST_BOT_TOKEN"

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


if __name__ == "__main__":
    __token_key = TELEGRAM_BOT_TOKEN if MODE == "production" else TELEGRAM_TEST_BOT_TOKEN
    __token = os.environ.get(__token_key)
    if __token is None:
        print(f'can\'t find token for bot in env variable "{__token_key}"')
    else:
        __bot_controller = BotController(__token)
        __bot_controller.start()
