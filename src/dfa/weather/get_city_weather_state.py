import src.dfa as dfa
from src.api.weather import WeatherAPI, ResponseStatus
from src.parse.intent import Intent, Command


class GetCityWeatherState(dfa.BaseState):

    __disable_message = "Модуль погоды ушёл в отпуск и сейчас недоступен."
    __unavailable_message = "Сервер сейчас недоступен, попробуйте позже."
    __unknown_city_message = "Я не знаю такого города: {}"
    __weather_message = "Сейчас там {}. Температура {}°C, но ощущается как {}°C. Ветер дует со скоростью {} м/с."

    def __init__(self):
        super().__init__()
        self._command_handler[Command.WEATHER] = self.handle_weather_command
        self.__weather_api = WeatherAPI()
        if not self.__weather_api.enabled:
            self.move = self.__disable_move

    @property
    def is_technical_state(self) -> bool:
        return True

    def __disable_move(self, intent: Intent) -> dfa.MoveResponse:
        return dfa.MoveResponse(dfa.StartState(), self.__disable_message)

    def handle_weather_command(self, intent: Intent) -> dfa.MoveResponse:
        if "city" in intent.parameters:
            api_response = self.__weather_api.get_weather(intent.parameters["city"])
            next_state = dfa.StartState()
            if api_response.status == ResponseStatus.UNAVAILABLE:
                message = self.__unavailable_message
            elif api_response.status == ResponseStatus.NOT_FOUND:
                message = self.__unknown_city_message.format(intent.parameters["city"])
            else:
                desc = api_response.weather_description
                message = self.__weather_message.format(
                    desc.weather, desc.temperature, desc.feels_like, desc.wind_speed
                )
            return dfa.MoveResponse(next_state, message)
        return dfa.MoveResponse(dfa.AskCityState(), None)
