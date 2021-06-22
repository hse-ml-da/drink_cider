from typing import List

import src.dfa as dfa
from src.api.weather import WeatherAPI, ResponseStatus, WeatherDescription, WeatherTime
from src.parse.intent import Intent, Command


class GetCityWeatherState(dfa.BaseState):

    __disable_message = "Модуль погоды ушёл в отпуск и сейчас недоступен."
    __unavailable_message = "Сервер сейчас недоступен, попробуйте позже."
    __unknown_city_message = "Я не знаю такого города: {}"
    __today_weather_message = "Сейчас там {}. Температура {}°C, но ощущается как {}°C. Ветер дует со скоростью {} м/с."
    __tomorrow_weather_message = (
        "Завтра там будет {}. Температура {}°C, но ощущаться будет как {}°C. Ветер будет дуть со скоростью {} м/с."
    )
    __next_week_forecast = "А в течение следующей недели ожидается:"
    __forecast_message = "{}. {}. Температура {}°C, но ощущается как {}°C. Ветер дует со скоростью {} м/с."

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

    def __prepare_message(self, weather_descriptions: List[WeatherDescription], time: WeatherTime) -> str:
        if time == WeatherTime.TODAY:
            desc = weather_descriptions[0]
            return self.__today_weather_message.format(desc.weather, desc.temperature, desc.feels_like, desc.wind_speed)
        elif time == WeatherTime.TOMORROW:
            desc = weather_descriptions[1]
            return self.__tomorrow_weather_message.format(
                desc.weather, desc.temperature, desc.feels_like, desc.wind_speed
            )
        else:
            desc = weather_descriptions[0]
            message = [
                self.__today_weather_message.format(desc.weather, desc.temperature, desc.feels_like, desc.wind_speed),
                self.__next_week_forecast,
            ]
            for i, desc in enumerate(weather_descriptions[1:]):
                message.append(
                    self.__forecast_message.format(
                        str(i + 1), desc.weather.capitalize(), desc.temperature, desc.feels_like, desc.wind_speed
                    )
                )
            return "\n".join(message)

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
                message = self.__prepare_message(desc, intent.parameters["time"])
            return dfa.MoveResponse(next_state, message)
        return dfa.MoveResponse(dfa.AskCityState(), None)
