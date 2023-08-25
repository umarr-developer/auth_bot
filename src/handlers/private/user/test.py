import random
import asyncio

from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.chat_action import ChatActionSender

from src.handlers.private.user.start import menu
from src.keyboards.builder import asnwers_keyboard
from src.models import Question

router = Router()


class Test(StatesGroup):
    testing = State()


async def on_test(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if not data['questions']:
        await on_finish_test(callback, state)
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
        await callback.message.answer_photo(question.photo_id, caption=text, reply_markup=keyboard)
        return
    await callback.message.answer(text, reply_markup=keyboard)


async def on_finish_test(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = 'Тест завершен\n\n'\
        f'Ваш результат: {data["result"]} правильных из {data["count"]} ответов'
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text='Поделиться', url='tg://share')]
        ]
    )
    await state.clear()
    await callback.message.answer(text, reply_markup=keyboard)
    await menu(callback.message)


@router.message(F.text == 'Перейти к тесту', StateFilter(None))
async def on_start_test(message: types.Message):
    text = 'Нажмите <b>Запустить тест</b>, если готовы начинать его проходить\n\n'\
        'Если хотите отменить, то введите команду или нажмите на кнопку "Отмена"'
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(
                text='Запустить тест', callback_data='launch_test')]
        ]
    )
    await message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data == 'launch_test', StateFilter(None))
async def on_launch_test(callback: types.CallbackQuery, state: FSMContext, db, bot):
    await callback.message.edit_reply_markup()
    text = 'Идет загрузка теста'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         keyboard=[
                                             [types.KeyboardButton(
                                                 text='Отмена')]
                                         ])
    await callback.message.answer(text, reply_markup=keyboard)

    async with ChatActionSender.typing(chat_id=callback.message.chat.id, bot=bot):
        await asyncio.sleep(1)
        text = 'Загрузка теста завершена'
        questions = await Question.all(db)

        random.shuffle(questions)

        await state.set_state(Test.testing)
        await state.update_data(questions=questions, result=0, count=len(questions))
        await callback.message.answer(text)

    await on_test(callback, state)


@router.callback_query(Test.testing, F.data.startswith('true'))
async def on_true_testing(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    result = data['result']
    await state.update_data(result=result+1)
    await callback.message.edit_reply_markup()
    await on_test(callback, state)


@router.callback_query(Test.testing, F.data.startswith('false'))
async def on_false_testing(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await on_test(callback, state)


@router.message(Test.testing, F.text == 'Отмена')
@router.message(Test.testing, Command(commands=['cancel']))
async def on_cancel_test(message: types.Message, state: FSMContext):
    await state.clear()

    text = 'Отмена теста'
    await message.answer(text)
    await menu(message)
