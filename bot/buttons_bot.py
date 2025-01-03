from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Kwork")
    builder.button(text="FL.ru")
    builder.adjust(3, 2)

    return builder.as_markup(resize_keyboard=True)


def moderator_keyboard():
    builder = InlineKeyboardBuilder()
    buttons = [
        builder.button(text="➡️ Далее", callback_data="next_order"),
        builder.button(text="⬅️ Назад", callback_data="prev_order")
    ]
    return builder.as_markup(inline_keyboard=[buttons])