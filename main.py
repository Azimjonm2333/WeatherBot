import asyncio
from aiogram import types
from app.bot import setup_bot

async def main():
    bot, dp, logger = setup_bot()

    await bot.set_my_commands([
        types.BotCommand(command="start", description="❤️‍🔥 Запустить бота"),
    ])

    await bot.delete_webhook(drop_pending_updates=True)

    logger.info("Запуск бота")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
