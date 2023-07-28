from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from src.models import User


class UserMiddleware(BaseMiddleware):

    async def __call__(self,
                       handler,
                       event: types.Message | types.CallbackQuery,
                       data: dict) -> any:
        db = data.get('db')
        data['user'] = await User.get(db, event.from_user.id)
        return await handler(event, data)
