from aiogram import Bot, types
from aiogram.filters import BaseFilter
from src.config import Config


class AdminFilter(BaseFilter):

    async def __call__(self, get: types.Message | types.CallbackQuery, config: Config):
        return get.from_user.id in config.bot.admin_ids


class UserFilter(AdminFilter):

    async def __call__(self, get: types.Message | types.CallbackQuery, config: Config):
        return not await super().__call__(get, config)
