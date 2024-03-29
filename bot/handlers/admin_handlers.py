from aiogram import F, Router, types
from aiogram.filters import CommandStart
from filters.filters import URLFilter
from keyboards.keyboards import generation_inline_kb
from texts.msg_text import TextMessage
from texts.texts_for_bot_buttons import ButtonData

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command_processing(message: types.Message):
    """Хендлер, срабатывающий на команду /start."""
    await message.delete()
    kb = generation_inline_kb(
        [
            ButtonData.show_my_resources,
            ButtonData.test_all_resources,
            ButtonData.add_resource,
        ],
        1,
    )
    return await message.answer(
        text=f'{message.from_user.first_name}{TextMessage.start_msg}',
        reply_markup=kb.as_markup(),
    )


@router.callback_query(F.data == ButtonData.back_to_main.callback_data)
async def back_to_main_button_processing(callback: types.CallbackQuery):
    """Хендлер, срабатывающий на нажатие кнопки 'Назад'."""
    kb = generation_inline_kb(
        [
            ButtonData.show_my_resources,
            ButtonData.test_all_resources,
            ButtonData.add_resource,
        ],
        1,
    )
    return await callback.message.edit_text(
        text=f'{callback.from_user.first_name}{TextMessage.start_msg}',
        reply_markup=kb.as_markup(),
    )


@router.callback_query(F.data == ButtonData.test_all_resources.callback_data)
async def test_all_resources_button_processing(callback: types.CallbackQuery):
    """Хендлер, срабатывающий на нажатие кнопки 'Тест всех ресурсов'."""
    kb = generation_inline_kb([ButtonData.back_to_main], 1)
    text = callback.data
    return await callback.message.edit_text(
        text=text, reply_markup=kb.as_markup()
    )


@router.callback_query(F.data == ButtonData.add_resource.callback_data)
async def add_resource_button_processing(callback: types.CallbackQuery):
    """Хендлер, срабатывающий на нажатие кнопки 'Добавить ресурс'."""
    kb = generation_inline_kb([ButtonData.back_to_main], 1)
    text = callback.data
    return await callback.message.edit_text(
        text=text, reply_markup=kb.as_markup()
    )


@router.callback_query(F.data == ButtonData.show_my_resources.callback_data)
async def show_my_resources_button_processing(callback: types.CallbackQuery):
    """Хендлер, срабатывающий на нажатие кнопки 'Отслеживаемые ресурсы'."""
    kb = generation_inline_kb([ButtonData.back_to_main], 1)
    text = callback.data
    return await callback.message.edit_text(
        text=text, reply_markup=kb.as_markup()
    )


@router.message(URLFilter())
async def entered_url_processing(message: types.Message, url: str):
    """
    Хендлер, обрабатывающий введенный пользователем URL
    для добавления его в писок отслеживаемых ресурсов.
    """
    text = 'Все верно, это нормальный ресурс'
    return await message.answer(text=text)


@router.message()
async def unprocessed_messages(message: types.Message):
    """Хендлер, срабатывающий на необработанные сообщения."""
    await message.reply(
        text=f'{message.from_user.first_name}{TextMessage.wrong_input_msg}'
    )
    kb = generation_inline_kb(
        [
            ButtonData.show_my_resources,
            ButtonData.test_all_resources,
            ButtonData.add_resource,
        ],
        1,
    )
    return await message.answer(
        text=f'{message.from_user.first_name}{TextMessage.start_msg}',
        reply_markup=kb.as_markup(),
    )
