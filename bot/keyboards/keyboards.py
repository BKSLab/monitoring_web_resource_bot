from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
from texts.texts_for_bot_buttons import InlineButtonData


def generation_inline_kb(
    data_for_buttons: list[InlineButtonData], width: int
) -> KeyboardBuilder[InlineKeyboardButton]:
    """Функция генерации inline клавиатур на основе полученных данных."""
    bt_list = [
        InlineKeyboardButton(
            text=inline_button_data.text,
            callback_data=inline_button_data.callback_data,
        )
        for inline_button_data in data_for_buttons
    ]
    return InlineKeyboardBuilder().row(*bt_list, width=width)
