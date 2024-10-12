import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    TELEGRAM_API_TOKEN: str = os.getenv('TELEGRAM_API_TOKEN')
    WEATHER_API_KEY: str = os.getenv('OPEN_WEATHER_API_KEY')
    WEATHER_CURRENT_URL: str = 'http://api.openweathermap.org/data/2.5/weather'
    WEATHER_FORECAST_URL: str = 'http://api.openweathermap.org/data/2.5/forecast'
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
