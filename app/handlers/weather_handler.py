from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.services.weather_service import WeatherService
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

router = Router()

def escape_city_name(city: str) -> str:
    """Заменяет пробелы на подчеркивания для безопасной передачи в callback_data."""
    return city.replace(' ', '_')

def unescape_city_name(city: str) -> str:
    """Возвращает оригинальное название города, заменяя подчеркивания на пробелы."""
    return city.replace('_', ' ')

def get_forecast_keyboard(city: str) -> InlineKeyboardMarkup:
    escaped_city = escape_city_name(city)
    callback_data = f"forecast_5_days_{escaped_city}"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 Посмотреть на 5 дней", callback_data=callback_data)]
    ])
    return keyboard


class WeatherHandler:
    def __init__(self, router: Router, weather_service: WeatherService):
        self.router = router
        self.weather_service = weather_service
        self.setup_handlers()


    def setup_handlers(self):
        self.router.message.register(self.send_welcome, Command(commands=["start"]))
        self.router.message.register(self.handle_city, F.text)
        self.router.callback_query.register(self.handle_forecast, F.data.startswith("forecast_5_days_"))


    async def send_welcome(self, message: Message):
        await message.answer(
            "Привет! Я бот, который показывает текущую погоду.\n"
            "Введите название города, и я покажу вам погоду."
        )


    async def handle_city(self, message: Message):
        city = message.text.strip()
        logger.info(f"Получен запрос погоды для города: {city}")
        weather = await self.weather_service.fetch_current_weather(city)
        if weather:
            response = (
                f"🌤 *Погода в городе {weather['city']}*:\n"
                f"🌡 Температура: {weather['temperature']}°C\n"
                f"💧 Влажность: {weather['humidity']}%\n"
                f"📝 Описание: {weather['description'].capitalize()}"
            )
            keyboard = get_forecast_keyboard(weather['city'])
            await message.answer(response, parse_mode="Markdown", reply_markup=keyboard)
        else:
            await message.answer("❌ Не удалось получить данные о погоде. Проверьте название города и попробуйте снова.")


    async def handle_forecast(self, callback_query: types.CallbackQuery):
        callback_data = callback_query.data
        try:
            _, _, escaped_city = callback_data.partition("forecast_5_days_")
            city = unescape_city_name(escaped_city)
        except Exception as e:
            logger.error(f"Ошибка при разборе callback_data: {e}")
            await callback_query.message.answer("❌ Некорректный запрос прогноза.")
            await callback_query.answer()
            return

        logger.info(f"Получен запрос прогноза погоды на 5 дней для города: {city}")
        forecast = await self.weather_service.fetch_forecast_weather(city)
        if forecast:
            forecast_by_day = defaultdict(list)
            for entry in forecast:
                date = entry['datetime'].split(' ')[0]
                forecast_by_day[date].append(entry)

            response = f"🌤 *Прогноз погоды на 5 дней в городе {city}:*\n"
            for date, entries in list(forecast_by_day.items())[:5]:
                daily_temps = [e['temperature'] for e in entries]
                daily_descriptions = [e['description'] for e in entries]
                avg_temp = sum(daily_temps) / len(daily_temps)
                most_common_desc = max(set(daily_descriptions), key=daily_descriptions.count)
                response += (
                    f"\n📅 *{date}*\n"
                    f"🌡 Средняя температура: {avg_temp:.1f}°C\n"
                    f"💧 Влажность: {entries[0]['humidity']}%\n"
                    f"📝 Описание: {most_common_desc.capitalize()}\n"
                )
            await callback_query.message.answer(response, parse_mode="Markdown")
        else:
            await callback_query.message.answer("❌ Не удалось получить прогноз погоды.")
        await callback_query.answer()
