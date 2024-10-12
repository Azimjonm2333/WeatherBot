# Telegram Weather Bot

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![aiogram](https://img.shields.io/badge/aiogram-3.0.0b12-green.svg)
![Docker](https://img.shields.io/badge/Docker-19.03.12-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)	

## Описание

**Telegram Weather Bot** — это Telegram-бот, предоставляющий актуальную информацию о погоде в любом городе. Бот интегрирован с API [OpenWeatherMap](https://openweathermap.org/) и разработан с использованием **aiogram** и принципов чистой архитектуры для обеспечения масштабируемости и удобства поддержки.

## Возможности

- Получение текущей погоды по названию города
- Отображение температуры, влажности и описания погодных условий
- Просмотр прогноза погоды на 5 дней
- Логирование событий и ошибок
- Контейнеризация с использованием Docker

## Требования

- Python 3.10+
- Docker (для контейнеризации)
- Учётная запись в Telegram и созданный бот через [BotFather](https://t.me/BotFather)
- API ключ от [OpenWeatherMap](https://openweathermap.org/)

## Установка

### Шаг 1: Клонирование Репозитория

```bash
git clone https://github.com/Azimjonm2333/WeatherBot.git
cd WeatherBot
```

### Шаг 2: Создание и Активация Виртуального Окружения

```bash
python3 -m venv venv
# Для Windows
venv\Scripts\activate
# Для Unix или MacOS
source venv/bin/activate
```

### Шаг 3: Установка Зависимостей

Используйте `pip` для установки зависимостей. Если вы используете другой пакетный менеджер, замените команды соответствующим образом.

```bash
pip install -r requirements.txt
```

### Шаг 4: Настройка Переменных Окружения

1. Создайте файл `.env`, скопировав содержимое `example.env`:

```bash
cp example.env .env
```
2. Откройте `.env` и заполните его вашими ключами:

```env
TELEGRAM_API_TOKEN=
OPEN_WEATHER_API_KEY=
```

### Шаг 5: Запуск Бота

#### Без использования Docker

Активируйте виртуальное окружение и запустите бота:

```bash
python main.py
```

#### С использованием Docker

##### 1. Сборка Docker-образа

```bash
docker build -t weather-bot .
```

##### 2. Запуск Docker-контейнера

Убедитесь, что файл `.env` настроен. Затем выполните:

```bash
docker run -d --env-file .env --name weather-bot weather-bot
```

##### 3. Просмотр логов

```bash
docker logs -f weather-bot
```

##### 4. Остановка и Удаление Контейнера

```bash
docker stop weather-bot
docker rm weather-bot
```

## Использование

1. **Старт бота**: Отправьте команду `/start`, чтобы получить приветственное сообщение.
2. **Запрос погоды**: Введите название города (например, `Москва`), и бот ответит текущей погодой с кнопкой для просмотра прогноза на 5 дней.
3. **Просмотр прогноза на 5 дней**: Нажмите на кнопку "📅 Посмотреть на 5 дней", и бот отправит прогноз погоды на 5 дней.
