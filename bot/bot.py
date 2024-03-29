import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from config_data.config import config
from data.database import create_table
from handlers import admin_handlers


async def main() -> None:
    create_table(
        db_name=config.db_name.get_secret_value(),
        table_name=config.table_name.get_secret_value(),
    )
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(admin_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename=(Path(__file__) / 'main.log').name,
        format=('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s'),
        filemode='w',
        encoding='utf-8',
    )
    asyncio.run(main())
