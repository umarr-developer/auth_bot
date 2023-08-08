import asyncio

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.chat_action import ChatActionSender

from src.models import Question, User

router = Router()


class Test(StatesGroup):
    testing = State()


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
async def on_laucnh_test(callback: types.CallbackQuery, state: FSMContext, db, bot):
    text = 'Идет загрузка теста'
    await callback.message.edit_text(text)

    async with ChatActionSender.typing(chat_id=callback.message.chat.id, bot=bot):
        await asyncio.sleep(1)
        text = 'Загрузка теста завершена'
        questions = await Question.all(db)

        await state.set_state(Test.testing)
        await state.update_data({'questions': questions})
        await callback.message.answer(text)
    
    await on_test(callback, state)


@router.callback_query()
async def on_test(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    question = data['questions'][0][0]

    description = question.description
    answers = question.answers

    text = f'Вопрос: {description}'
    await callback.message.answer(text)
    # TODO
