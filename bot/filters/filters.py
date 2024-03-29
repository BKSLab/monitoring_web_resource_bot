import re

from aiogram.filters import BaseFilter
from aiogram.types import Message


class URLFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        pattern = r'(https?://[^\"\s]+)'
        if re.fullmatch(pattern, message.text):
            return {'url': message.text}
        return False


# pattern = (
# r'/^((http|https):\/\/)?(([A-Z0-9][A-Z0-9_-]*)(\.[A-Z0-9][A-Z0-9_-]*)+)/i'
# )
# pattern = r'/https?:\/\/\S+\.\S+/g'
# pattern = r'/(https?:\/\/)?(www\.)?\S+\.\S+/g'
# pattern = r"^(https?:\/\/)?([\w-]{1,32}\.[\w-]{1,32})[^\s@]* + @"
