from aiogram import types
from aiogram.filters import BaseFilter


class ChatTypeFilter(BaseFilter):

    chat_types: list[str] = []

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types


class PrivateTypeFilter(ChatTypeFilter):
    chat_types: list[str] = ['private']


class GroupTypeFilter(ChatTypeFilter):
    chat_types: list[str] = ['group', 'supergroup']
