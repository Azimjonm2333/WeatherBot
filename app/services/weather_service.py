import aiohttp
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self, api_key: str, current_url: str, forecast_url: str):
        self.api_key = api_key
        self.current_url = current_url
        self.forecast_url = forecast_url

    async def fetch_current_weather(self, city_name: str) -> Optional[Dict]:
        params = {
            'q': city_name,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'ru'
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.current_url, params=params) as response:
                    if response.status != 200:
                        text = await response.text()
                        logger.error(f"HTTP ошибка: {response.status} - Ответ: {text}")
                        return None
                    data = await response.json()
                    weather = {
                        'city': data.get('name'),
                        'temperature': data['main']['temp'],
                        'humidity': data['main']['humidity'],
                        'description': data['weather'][0]['description']
                    }
                    logger.info(f"Получена текущая погода для города {city_name}: {weather}")
                    return weather
        except aiohttp.ClientError as http_err:
            logger.error(f"HTTP ошибка: {http_err}")
        except Exception as err:
            logger.error(f"Ошибка при получении текущей погоды: {err}")
        return None


    async def fetch_forecast_weather(self, city_name: str) -> Optional[List[Dict]]:
        params = {
            'q': city_name,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'ru'
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.forecast_url, params=params) as response:
                    if response.status != 200:
                        text = await response.text()
                        logger.error(f"HTTP ошибка: {response.status} - Ответ: {text}")
                        return None
                    data = await response.json()
                    forecast_list = data.get('list', [])
                    forecast = []
                    for item in forecast_list:
                        forecast.append({
                            'datetime': item['dt_txt'],
                            'temperature': item['main']['temp'],
                            'humidity': item['main']['humidity'],
                            'description': item['weather'][0]['description']
                        })
                    logger.info(f"Получен прогноз погоды для города {city_name}: {forecast}")
                    return forecast
        except aiohttp.ClientError as http_err:
            logger.error(f"HTTP ошибка: {http_err}")
        except Exception as err:
            logger.error(f"Ошибка при получении прогноза погоды: {err}")
        return None
