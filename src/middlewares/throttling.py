from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):

    default_rate = 1

    def __init__(self, rate: int | None = None):
        self.rate = TTLCache(maxsize=1024, ttl=rate or self.default_rate)

    async def __call__(self,
                       handler,
                       event: types.Message,
                       data: dict) -> any:
        if event.chat.id in self.rate:
            self.rate[event.chat.id] = None
            return
        self.rate[event.chat.id] = None
        return await handler(event, data)
