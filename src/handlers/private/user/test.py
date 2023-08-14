import asyncio

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.chat_action import ChatActionSender

from src.keyboards.builder import asnwers_keyboard
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
        await state.update_data(questions=questions, result=0)
        await callback.message.answer(text)

    await on_test(callback, state)


async def on_test(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if not data['questions']:
        await state.clear()
        text = f'Конец теста, ваш результат: {data["result"]}'
        await callback.message.answer(text)
        return

    questions: list = data['questions']
    question: Question = questions[0][0]
    await state.update_data(questions=questions)
    questions.pop(0)

    description = question.description
    answers = question.answers
    text = f'Вопрос: {description}'
    keyboard = asnwers_keyboard(answers)

    if question.photo_id:
        await callback.message.reply_photo(question.photo_id, caption=text, reply_markup=keyboard)
        return
    await callback.message.answer(text, reply_markup=keyboard)


@router.callback_query(Test.testing, F.data == 'true')
async def on_true_testing(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    result = data['result']
    await state.update_data(result=result+1)
    await on_test(callback, state)


@router.callback_query(Test.testing, F.data == 'false')
async def on_false_testing(callback: types.CallbackQuery, state: FSMContext):
    await on_test(callback, state)
