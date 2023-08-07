from aiogram import F, Router, types

router = Router()



@router.message(F.text == 'О боте')
async def on_about(message: types.Message):
    text = 'Информация о боте'
    await message.answer(text)

