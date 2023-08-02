import asyncio
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionSender
from src.models.user import User

router = Router()


@router.message(F.text == 'Перейти к тесту')
async def on_test(message: types.Message, db, user: tuple[User]):
    text = 'Нажмите <b>Запустить тест</b>, если готовы начинать его проходить'
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(
                text='Запустить тест', callback_data='launch_test')]
        ]
    )
    await message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data == 'launch_test')
async def on_laucnh_test(callback: types.CallbackQuery, bot):
    text = 'Идет загрузка теста'
    await callback.message.edit_text(text)

    async with ChatActionSender.typing(bot=bot, chat_id=callback.message.chat.id):
        await asyncio.sleep(1)
        text = 'Тест!'
        await callback.message.answer(text)
