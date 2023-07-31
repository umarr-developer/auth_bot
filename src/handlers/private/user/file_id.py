from aiogram import F, Router, types

router = Router()


@router.message(F.photo, F.caption == '+')
async def on_get_file_id(message: types.Message):
    print(message.caption)
    await message.answer(text=f'<code>{message.photo[-1].file_id}</code>')
