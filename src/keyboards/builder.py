from aiogram import types


def asnwers_keyboard(buttons: dict) -> types.InlineKeyboardMarkup:
    inline_buttons = list()
    for key in buttons:
        for value in buttons[key]:
            inline_buttons.append(
                [types.InlineKeyboardButton(text=value, callback_data=key)])
    return types.InlineKeyboardMarkup(
        inline_keyboard=inline_buttons
    )


# print(asnwers_keyboard({'true': ['23'], 'false': ['213']}))
