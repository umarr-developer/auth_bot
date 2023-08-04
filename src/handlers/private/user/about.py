from aiogram import F, Router, types
from aiogram.filters import Command

from src.models.user import User

router = Router()



@router.message(F.text == 'О боте')
async def on_about(message: types.Message, db, user: tuple[User]):
    text = 'Информация о боте'
    await message.answer(text)

