from aiogram import Bot, Dispatcher
from app.config import Config
from app.handlers.weather_handler import WeatherHandler
from app.services.weather_service import WeatherService
from app.utils.logger import setup_logger
import logging

def setup_bot() -> tuple[Bot, Dispatcher, logging.Logger]:
    logger = setup_logger()
    logger.info("Инициализация бота")

    bot = Bot(token=Config.TELEGRAM_API_TOKEN)
    dp = Dispatcher()

    weather_service = WeatherService(
        api_key=Config.WEATHER_API_KEY,
        current_url=Config.WEATHER_CURRENT_URL,
        forecast_url=Config.WEATHER_FORECAST_URL
    )

    WeatherHandler(router=dp, weather_service=weather_service)

    return bot, dp, logger
