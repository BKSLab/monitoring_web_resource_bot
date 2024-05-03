import re

from aiogram import types
from aiogram.filters import BaseFilter
from config_data.config import config
from data.database import exists_url


class URLFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        pattern = r'(https?://[^\"\s]+)'
        if re.fullmatch(pattern, message.text):
            return True
        return False


class DeleteURLFilter(BaseFilter):
    async def __call__(self, callback: types.CallbackQuery) -> bool:
        data = callback.data.split('_del_')
        if data[0] == 'delete' and data[1] == 'allresources':
            return {
                'url': None,
                'action': 'delete_all',
            }
        if data[0] == 'delete' and data[1] != 'allresources':
            return {
                'url': data[1],
                'action': 'delete_one',
            }
        return False


class TestURLFilter(BaseFilter):
    async def __call__(self, callback: types.CallbackQuery) -> bool:
        data = callback.data.split('_tes_')
        if data[0] != 'test':
            return False
        query_result = exists_url(
            db_name=config.db_name.get_secret_value(),
            table_name=config.table_name.get_secret_value(),
            url=data[1],
            tg_user_id=callback.from_user.id,
        )
        if query_result:
            return {'url': data[1]}
        return False
