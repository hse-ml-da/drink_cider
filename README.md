# Drink cider bot
Telegram bot for cider recommendation, weather request, and simply chatting.

## Installation and running
1. Clone the repo:
```shell
git clone https://github.com/hse-ml-da/drink_cider.git
cd drink_cider
```
2. Install requirements

Create or activate virtual env if needed
```shell
pip install -r requirements.txt
```
3. Receive necessary API tokens
- **Telegram bor API token**.
Navigate to [@BotFather](https://t.me/BotFather), create a new bot and receive its API token.
- **OpenWeather API token**.
To enable getting weather forecast inside bot you should receive API token from [OpenWeather](https://openweathermap.org).
Create profile and then create API in corresponding tab.
4. Download weights for dialogue module

Download quantized model weigths from [s3](https://voudy-data.s3.eu-north-1.amazonaws.com/dialogpt2_quant.pth)
   and place them in [src/resources](src/resources).

5. Start bot

Inside your virtual environment run
```shell
TELEGRAM_BOT_TOKEN=<telegram api token> OPEN_WEATHER_API_KEY=<openweather api token> PYTHONPATH=. python src/main.py
```
For convenience, API tokens can be exported to environment variables.
