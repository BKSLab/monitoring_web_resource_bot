from aiogram import Bot

from request_to_url.request_to_url import get_request_url
from data.database import get_all_rows
from config_data.config import config


async def scheduled_request(bot: Bot) -> None:
    """
    Тест всех ресурсов, имеющихся в БД
    """
    urls = get_all_rows(
        db_name=config.db_name.get_secret_value(),
        table_name=config.table_name.get_secret_value(),
    )
    for url in urls:
        result = get_request_url(url[1])
        if not result.get('status'):
            text = (
                f'Есть проблемы проблемы с доступностью url: {url[1]}\n'
                f'Текст ошибки: {result.get("message_error")}'
            )
            await bot.send_message(
                chat_id=url[2],
                text=text,
            )
