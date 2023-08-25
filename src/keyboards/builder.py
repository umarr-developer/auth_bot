import random

from aiogram import types


def asnwers_keyboard(buttons: dict) -> types.InlineKeyboardMarkup:
    inline_buttons = list()
    index = 0
    for key in buttons:
        for value in buttons[key]:
            inline_buttons.append(
                [types.InlineKeyboardButton(text=value, callback_data=key + str(index))])
            index += 1

    random.shuffle(inline_buttons)

    return types.InlineKeyboardMarkup(
        inline_keyboard=inline_buttons
    )
