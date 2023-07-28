from aiogram import Bot, types


async def set_commands(bot: Bot):
    await bot.set_my_commands(commands=[
        types.BotCommand(command='start', description='Запустить бота')
    ],
    scope=types.BotCommandScopeAllPrivateChats()
)
