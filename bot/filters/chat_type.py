import aiogram
import aiogram.filters

from icecream import ic

#create new filter for chat type define
class ChatTypeFilter(aiogram.filters.Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: aiogram.types.Message) -> bool:
        return message.chat.type in self.chat_types