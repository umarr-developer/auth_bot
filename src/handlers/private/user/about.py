from aiogram import F, Router, types
from aiogram.filters import StateFilter

router = Router()



@router.message(F.text == 'О боте', StateFilter(None))
async def on_about(message: types.Message):
    text = 'Информация о боте'
    await message.answer(text)

