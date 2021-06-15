from src.intent.intent import Intent, Command


def parse(message: str) -> Intent:
    normalized_message = message.strip().lower()
    if normalized_message == "погода":
        return Intent(Command.WEATHER, message)
    else:
        return Intent(Command.UNKNOWN, message)
