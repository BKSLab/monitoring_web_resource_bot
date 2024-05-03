from aiogram import F, Router, types
from aiogram.filters import CommandStart
from config_data.config import config
from data.database import (
    add_data_to_table,
    deleting_one_row_for_user,
    deleting_rows_for_user,
    get_all_rows_for_user,
)
from filters.filters import DeleteURLFilter, TestURLFilter, URLFilter
from keyboards.keyboards import generation_inline_kb
from request_to_url.request_to_url import get_request_url
from texts.msg_text import TextMessage
from texts.texts_for_bot_buttons import ButtonData, InlineButtonData

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
    text = TextMessage.start_msg.format(message.from_user.first_name)
    return await message.answer(
        text=text,
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
    text = TextMessage.start_msg.format(callback.from_user.first_name)
    return await callback.message.edit_text(
        text=text,
        reply_markup=kb.as_markup(),
    )


@router.callback_query(F.data == ButtonData.add_resource.callback_data)
async def add_resource_button_processing(callback: types.CallbackQuery):
    """Хендлер, срабатывающий на нажатие кнопки 'Добавить ресурс'."""
    kb = generation_inline_kb(
        [
            ButtonData.back_to_main,
        ],
        1,
    )
    text = TextMessage.add_resource.format(callback.from_user.first_name)
    await callback.message.edit_text(text=text, reply_markup=kb.as_markup())


@router.message(URLFilter())
async def entered_url_processing(message: types.Message):
    """
    Хендлер, обрабатывающий введенный пользователем URL
    для добавления его в список отслеживаемых ресурсов.
    """
    await message.delete()
    query_result = add_data_to_table(
        db_name=config.db_name.get_secret_value(),
        table_name=config.table_name.get_secret_value(),
        url=message.text,
        tg_user_id=message.from_user.id,
    )
    if not query_result.get('status'):
        text = query_result.get('message_error')
        kb = generation_inline_kb(
            [
                ButtonData.show_my_resources,
                ButtonData.add_resource,
                ButtonData.back_to_main,
            ],
            1,
        )
        return await message.answer(text=text, reply_markup=kb.as_markup())
    text = TextMessage.success.format(
        message.from_user.first_name,
        message.text,
    )
    kb = generation_inline_kb(
        [
            ButtonData.show_my_resources,
            ButtonData.add_resource,
            ButtonData.back_to_main,
        ],
        1,
    )
    return await message.answer(text=text, reply_markup=kb.as_markup())


@router.callback_query(F.data == ButtonData.show_my_resources.callback_data)
async def show_my_resources_button_processing(callback: types.CallbackQuery):
    """Хендлер, срабатывающий на нажатие кнопки 'Мои ресурсы'."""
    urls = get_all_rows_for_user(
        db_name=config.db_name.get_secret_value(),
        table_name=config.table_name.get_secret_value(),
        tg_user_id=callback.from_user.id,
    )
    count = len(urls)
    if count == 0:
        text = TextMessage.no_resource.format(callback.from_user.first_name)
        kb = generation_inline_kb(
            [
                ButtonData.add_resource,
                ButtonData.back_to_main,
            ],
            1,
        )
        return await callback.message.edit_text(
            text=text, reply_markup=kb.as_markup()
        )

    text = f'Мои ресурсы: {count}'
    await callback.message.edit_text(text=text)

    for url in urls:
        text = f'url: {url[1]}'
        kb = generation_inline_kb(
            [
                InlineButtonData('Удалить URL', f'delete_del_{url[1]}'),
                InlineButtonData('Тест URL', f'test_tes_{url[1]}'),
            ],
            2,
        )
        await callback.message.answer(text=text, reply_markup=kb.as_markup())
    text = 'Дополнительные действия:'
    kb = generation_inline_kb(
        [
            ButtonData.add_resource,
            ButtonData.test_all_resources,
            ButtonData.delete_all_resources,
            ButtonData.back_to_main,
        ],
        1,
    )
    await callback.message.answer(text=text, reply_markup=kb.as_markup())


@router.callback_query(DeleteURLFilter())
async def del_resource_button_processing(
    callback: types.CallbackQuery,
    url: str | None,
    action: str,
):
    """Хендлер, срабатывающий на нажатие кнопки 'Удалить URL'."""
    if action == 'delete_one':
        deleting_one_row_for_user(
            db_name=config.db_name.get_secret_value(),
            table_name=config.table_name.get_secret_value(),
            url=url,
            tg_user_id=callback.from_user.id,
        )
        text = 'URL ууспешно удален'
        return await callback.message.edit_text(text=text)
    if action == 'delete_all':
        deleting_rows_for_user(
            db_name=config.db_name.get_secret_value(),
            table_name=config.table_name.get_secret_value(),
            tg_user_id=callback.from_user.id,
        )
        text = TextMessage.deleting_all_resources
        kb = generation_inline_kb(
            [
                ButtonData.add_resource,
                ButtonData.back_to_main,
            ],
            1,
        )
        return await callback.message.edit_text(
            text=text, reply_markup=kb.as_markup()
        )


@router.callback_query(TestURLFilter())
async def test_resources_button_processing(
    callback: types.CallbackQuery,
    url: str,
):
    """Хендлер, срабатывающий на нажатие кнопки"""
    await callback.answer()
    result = get_request_url(url)
    if not result.get('status'):
        message_error = result.get('message_error')
        text = f'При запросе к URL: {url} получена ошибка:\n\n{message_error}'
        kb = generation_inline_kb(
            [
                ButtonData.show_my_resources,
                ButtonData.back_to_main,
            ],
            1,
        )
        return await callback.message.answer(
            text=text, reply_markup=kb.as_markup()
        )
    responce = result.get('responce')
    code = responce.status_code
    text = f'Код ответа при get запросе к URL: {url}: {code}'
    kb = generation_inline_kb(
        [
            ButtonData.show_my_resources,
            ButtonData.back_to_main,
        ],
        1,
    )
    return await callback.message.answer(
        text=text, reply_markup=kb.as_markup()
    )


@router.callback_query(F.data == ButtonData.test_all_resources.callback_data)
async def test_all_resources_button_processing(callback: types.CallbackQuery):
    """Хендлер, срабатывающий на нажатие кнопки 'Тест всех ресурсов'."""
    await callback.answer()
    query_result = get_all_rows_for_user(
        db_name=config.db_name.get_secret_value(),
        table_name=config.table_name.get_secret_value(),
        tg_user_id=callback.from_user.id,
    )
    if not query_result:
        text = TextMessage.no_resource.format(callback.from_user.first_name)
        kb = generation_inline_kb(
            [
                ButtonData.add_resource,
                ButtonData.back_to_main,
            ],
            1,
        )
        return await callback.message.edit_text(
            text=text, reply_markup=kb.as_markup()
        )
    for row in query_result:
        result = get_request_url(row[1])
        if not result.get('status'):
            message_error = result.get('message_error')
            text = (
                f'При запросе к URL: {row[1]} получена '
                f'ошибка:\n\n{message_error}'
            )
            await callback.message.answer(text=text)
        if result.get('status'):
            responce = result.get('responce')
            code = responce.status_code
            text = f'Код ответа при get запросе к URL: {row[1]}: {code}'
            await callback.message.answer(text=text)
    text = f'Всего протестировано {len(query_result)} URL адресов'
    kb = generation_inline_kb(
        [
            ButtonData.show_my_resources,
            ButtonData.back_to_main,
        ],
        1,
    )
    await callback.message.answer(text=text, reply_markup=kb.as_markup())


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
