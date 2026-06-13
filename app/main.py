import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from app.telegram_bot.handlers import user_client
from app.telegram_bot.lexicon.lexicon import LEXICON_RU

# Настраиваем логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    # Загружаем переменные окружения (.env)
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")

    logger.info(LEXICON_RU["log_bot_starting"])

    # Инициализируем бота и диспетчер
    bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Регистрируем роутеры
    dp.include_router(user_client.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info(LEXICON_RU["log_bot_started"])
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())