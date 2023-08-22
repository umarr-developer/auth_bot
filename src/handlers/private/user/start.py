from aiogram import Router, types
from aiogram.filters import Command, StateFilter

from src.models import User

router = Router()


async def menu(message: types.Message | types.CallbackQuery):
    text = 'Выберите действие'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [types.KeyboardButton(text='Перейти к тесту')],
        [types.KeyboardButton(text='О боте')]
    ])
    await message.answer(text, reply_markup=keyboard)


@router.message(Command(commands=['start']), StateFilter(None))
async def on_start(message: types.Message, db):
    user = await User.get(db, user_id=message.from_user.id)
    if not user:
        user = await User.new(db, user_id=message.from_user.id)
    text = f'Добро пожаловать, <b>{message.from_user.first_name}</b>'
    await message.answer(text)
    await menu(message)
