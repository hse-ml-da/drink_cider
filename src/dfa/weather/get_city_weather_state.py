from datetime import datetime
from typing import List, Dict

import src.dfa as dfa
from src.api.weather import WeatherAPI, ResponseStatus, WeatherDescription, WeatherTime
from src.parse.intent import Intent, Command


class GetCityWeatherState(dfa.BaseState):

    _disable_message = "Модуль погоды ушёл в отпуск и сейчас недоступен."
    __unavailable_message = "Сервер сейчас недоступен, попробуйте позже."
    __unknown_city_message = "Я не знаю такого города: {}"
    __today_weather_message = "Сейчас там {}. Температура {}°C, но ощущается как {}°C. Ветер дует со скоростью {} м/с."
    __tomorrow_weather_message = (
        "Завтра там будет {}. Температура {}°C, но ощущаться будет как {}°C. Ветер будет дуть со скоростью {} м/с."
    )
    __next_week_forecast = "А вот прогноз на следующую неделю."
    __forecast_message = (
        "{} там будет {}. Температура {}°C, но ощущаться будет как {}°C. Ветер будет дуть со скоростью {} м/с."
    )
    __weekdays = ["В понедельник", "Во вторник", "В среду", "В четверг", "В пятницу", "В субботу", "В воскресенье"]

    def __init__(self):
        super().__init__()
        self._command_handler[Command.WEATHER] = self.handle_weather_command
        self.__weather_api = WeatherAPI()
        if not self.__weather_api.enabled:
            self.move = self._disable_move

        self.__history: Dict[int, Intent] = {}

    @property
    def is_technical_state(self) -> bool:
        return True

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
            today_weekday = datetime.today().weekday()
            for i, desc in enumerate(weather_descriptions[1:]):
                weekday = self.__weekdays[(today_weekday + 1 + i) % len(self.__weekdays)]
                message.append(
                    self.__forecast_message.format(
                        weekday, desc.weather, desc.temperature, desc.feels_like, desc.wind_speed
                    )
                )
            return "\n".join(message)

    def handle_weather_command(self, intent: Intent, user_id: int) -> dfa.MoveResponse:
        if "city" in intent.parameters:
            api_response = self.__weather_api.get_weather(intent.parameters["city"])
            next_state = dfa.StartState()
            if api_response.status == ResponseStatus.UNAVAILABLE:
                message = self.__unavailable_message
            elif api_response.status == ResponseStatus.NOT_FOUND:
                message = self.__unknown_city_message.format(intent.parameters["city"])
            else:
                desc = api_response.weather_description
                if "time" in intent.parameters:
                    time = intent.parameters["time"]
                elif user_id in self.__history:
                    time = self.__history[user_id].parameters["time"]
                else:
                    time = WeatherTime.TODAY
                message = self.__prepare_message(desc, time)
            return dfa.MoveResponse(next_state, message)

        if "time" in intent.parameters:
            self.__history[user_id] = intent
        return dfa.MoveResponse(dfa.AskCityState(), None)
