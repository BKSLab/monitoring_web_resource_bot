import sqlite3

import pytest
from config_for_db import config_db
from utils import resource_data, table_structure

from bot.data.database import (
    add_data_to_table,
    create_table,
    deleting_one_row_for_user,
    deleting_rows_for_user,
    exists_url,
    get_all_rows,
    get_all_rows_for_user,
)


@pytest.mark.usefixtures('db_session')
def test_create_table(db_session: sqlite3.Cursor):
    """Тест функции создания таблицы в базе данных."""

    sql_query = 'SELECT name FROM sqlite_master WHERE type="table";'
    tables_before_create = db_session.execute(sql_query).fetchall()

    assert not tables_before_create, (
        f'В тестовой базе: {config_db.db_name_test.get_secret_value()} на момент '
        f'начала теста содержатся таблицы: {tables_before_create}.\n'
        'Убедитесь, что тестовая база создается правильно.'
    )

    table_name = config_db.table_name_test.get_secret_value()
    print(f'table_name {table_name}')
    create_table(
        db_name=config_db.db_name_test.get_secret_value(),
        table_name=table_name,
    )
    tables_after_created = [
        ''.join(table) for table in db_session.execute(sql_query).fetchall()
    ]

    assert table_name in tables_after_created, (
        f'Таблица с именем: {table_name} в тестовой базе отсутствует.\n'
        f'Убедитесь, что функция {create_table.__name__} в модуле '
        f'{create_table.__module__} работает правильно.'
    )

    sql_query = f'PRAGMA TABLE_INFO({table_name});'
    table_info = [inf[1:3] for inf in db_session.execute(sql_query).fetchall()]
    structure_created_table = {
        name: values
        for name, values in zip(table_structure.keys(), table_info)
    }

    assert structure_created_table == table_structure, (
        f'Таблица {table_name} имеет не верную структуру. '
        'Названия полей и их тип не соответствуют ТЗ.\n'
        f'Убедитесь, что функция {create_table.__name__} в модуле '
        f'{create_table.__module__} работает правильно.'
    )


@pytest.mark.usefixtures('db_session')
def test_add_data_to_table(db_session: sqlite3.Cursor):
    """Тест функции добавления данных в таблицу."""
    table_name = config_db.table_name_test.get_secret_value()
    sql_query = f'SELECT COUNT(*) FROM {table_name}'
    counds_records = db_session.execute(sql_query).fetchone()[0]

    assert counds_records == 0, (
        f'В таблице {table_name} на момент начала теста '
        'существуют записи.\nУбедитесь, что процесс создания '
        'тестовой таблице настроен правильно.'
    )

    url = 'https://touch-it.ru/'
    tg_user_id = 123456

    query_result = add_data_to_table(
        db_name=config_db.db_name_test.get_secret_value(),
        table_name=table_name,
        url=url,
        tg_user_id=tg_user_id,
    )

    sql_query = f'SELECT COUNT(*) FROM {table_name}'
    counds_records = db_session.execute(sql_query).fetchone()[0]

    assert counds_records == 1, (
        f'В тестовой таблице {table_name} на была создана  '
        f'новая запись.\nУбедитесь, что функция {add_data_to_table.__name__} '
        f'В модуле {add_data_to_table.__module__} работает правильно.'
    )
    assert isinstance(query_result, dict), (
        f'Возвращенный функцией {add_data_to_table.__name__} тип данных не '
        'соответствует ТЗ:\nфункция должна вернуть словарь, но вернула: '
        f'{type(query_result)}.\nУбедитесь, что функция '
        f'{add_data_to_table.__name__} возвращает правильных тип данных.'
    )
    assert all(key in query_result for key in ('status',)), (
        f'Функция {add_data_to_table.__name__} вернула словарь с ключами, '
        'которые не соответствуют ТЗ.\nУбедитесь, что функция '
        f'{add_data_to_table.__name__} работает правильно.'
    )
    assert query_result.get('status'), (
        f'Функция {add_data_to_table.__name__} при удачной попытке записи, '
        'Должна возвращать значение True в записе словаря с ключем "status"'
    )

    sql_query = f"""
            SELECT * FROM {table_name}
            WHERE url = ? AND tg_user_id = ?;
        """
    _, url_from_db, tg_user_id_from_db = db_session.execute(
        sql_query, (url, tg_user_id)
    ).fetchone()

    assert url_from_db == url and tg_user_id_from_db == tg_user_id, (
        f'При записи данных в таблицу {table_name} произошла ошибка. '
        f'Функция {add_data_to_table.__name__} сработала не корректно. '
        f'Записанные данные не соответствуют входным данным.'
    )

    result_two = add_data_to_table(
        db_name=config_db.db_name_test.get_secret_value(),
        table_name=table_name,
        url=url,
        tg_user_id=tg_user_id,
    )

    sql_query = f'SELECT COUNT(*) FROM {table_name}'
    counds_records = db_session.execute(sql_query).fetchone()[0]

    assert counds_records < 2, (
        f'В таблице {table_name} уже есть запись с таким url. '
        'Повторная запись запрещена. Проверьте правильность работы '
        f'функции {add_data_to_table.__name__}'
    )

    text_message_error = 'url https://touch-it.ru/ уже существует в БД'
    assert all(key in result_two for key in ('status', 'message_error')), (
        f'Функция {add_data_to_table.__name__} вернула словарь с ключами, '
        'которые не соответствуют ТЗ.\nУбедитесь, что функция '
        f'{add_data_to_table.__name__} работает правильно.'
    )
    assert not result_two.get('status'), (
        f'Функция {add_data_to_table.__name__} при неудачной попытке записи, '
        'Должна возвращать значение Falseв записе словаря с ключем "status"'
    )

    text_message_error = 'url https://touch-it.ru/ уже существует в БД'

    assert result_two.get('message_error') == text_message_error, (
        'Текст сообщения об ошибки при попытке повторной записи в БД '
        'не соответствует ТЗ.\nПроверьте правильность формирования '
        f'возвращаемого сообщения функцией {add_data_to_table.__name__}'
    )


@pytest.mark.usefixtures('db_session', 'insert_records_in_table')
def test_exists_url():
    """
    Тест функции проверяющей наличие в таблице URL
    пользователя перед его тестом.
    """
    table_name = config_db.table_name_test.get_secret_value()
    existing_url = resource_data[0][0]
    tg_user_id = resource_data[0][1]

    query_result = exists_url(
        db_name=config_db.db_name_test.get_secret_value(),
        table_name=table_name,
        url=existing_url,
        tg_user_id=tg_user_id,
    )
    assert query_result, (
        'Функция должна была вернуть запись, соответствующую '
        f'следующим данным: {resource_data[0]}. Проверьте работу '
        f'функции {exists_url.__name__}'
    )
    missing_url = 'https://www.google-shmugal.com/'
    tg_user_id = 111111
    query_result = exists_url(
        db_name=config_db.db_name_test.get_secret_value(),
        table_name=table_name,
        url=missing_url,
        tg_user_id=tg_user_id,
    )
    assert not query_result, (
        'Функция должна была вернуть False, так как получила на вход '
        'данные с отсутствующим URL в таблице ресурсов.'
        f'Проверьте работу функции {exists_url.__name__}'
    )


@pytest.mark.usefixtures('db_session', 'insert_records_in_table')
def test_get_all_rows():
    """
    Тест функции возвращающей все данные пользователей
    и отслеживаемых ими ресурсов.
    """
    table_name = config_db.table_name_test.get_secret_value()
    query_result = get_all_rows(
        db_name=config_db.db_name_test.get_secret_value(),
        table_name=table_name,
    )
    assert isinstance(query_result, list), (
        f'Функция {get_all_rows.__name__} должна вернуть '
        f'объект типа list. Функция вернула объект типа {type(query_result)}. '
        'Убедитесь, что функция работает правильно.'
    )
    assert len(query_result) == len(resource_data), (
        f'Количество записей в таблице {table_name} не совпадает с '
        'количество внесенных в таблицу тестовых записей. Проверьте '
        f'работу функции {get_all_rows.__name__}'
    )


@pytest.mark.usefixtures('db_session', 'insert_records_in_table')
def test_get_all_rows_for_user():
    """Тест функции, возвращающей все записи одно пользователля."""
    table_name = config_db.table_name_test.get_secret_value()
    tg_user_id = 111111

    query_result = get_all_rows_for_user(
        db_name=config_db.db_name_test.get_secret_value(),
        table_name=table_name,
        tg_user_id=tg_user_id,
    )
    assert isinstance(query_result, list), (
        f'Функция {get_all_rows_for_user.__name__} должна вернуть '
        f'объект типа list. Функция вернула объект типа {type(query_result)}. '
        'Убедитесь, что функция работает правильно.'
    )
    assert len(query_result) == 4, (
        f'Количество записей пользователя в таблице {table_name} '
        'не совпадает с количество внесенных в таблицу '
        'тестовых записей. Проверьте '
        f'работу функции {get_all_rows_for_user.__name__}'
    )
    assert all(row[2] == tg_user_id for row in query_result), (
        f'Функция {get_all_rows_for_user.__name__} вернула записи, '
        'принадлижащие разным пользователям. Функция должна возвращать записи '
        'принадлежащие пользователлю с заданным tg_user_id.'
    )


@pytest.mark.usefixtures('db_session', 'insert_records_in_table')
def test_deleting_all_user_resources():
    """
    Тест функции, удаляющей все записи об отслеживаемых
    ресурсах одного пользователя.
    """
    table_name = config_db.table_name_test.get_secret_value()
    db_name = config_db.db_name_test.get_secret_value()
    tg_user_id = 111111

    deleting_rows_for_user(
        db_name=db_name,
        table_name=table_name,
        tg_user_id=tg_user_id,
    )
    all_user_records_after_deletion = get_all_rows_for_user(
        db_name=db_name, table_name=table_name, tg_user_id=tg_user_id
    )
    assert not all_user_records_after_deletion, (
        f'Данные пользователя с tg_user_id: {tg_user_id} не были '
        f'удалены. Проверьте работу функции {deleting_rows_for_user.__name__}'
    )


@pytest.mark.usefixtures('db_session', 'insert_records_in_table')
def test_deleting_one_row_for_user(db_session: sqlite3.Cursor):
    """Тест функции удаления одной записи пользователя."""
    table_name = config_db.table_name_test.get_secret_value()
    db_name = config_db.db_name_test.get_secret_value()
    _, url, tg_user_id = get_all_rows(
        db_name=db_name,
        table_name=table_name,
    )[0]

    deleting_one_row_for_user(
        db_name=db_name, table_name=table_name, url=url, tg_user_id=tg_user_id
    )
    sql_query = f"""
            SELECT * FROM {table_name}
            WHERE url = ? AND tg_user_id = ?;
        """
    query_result_after_deletion = db_session.execute(
        sql_query, (url, tg_user_id)
    ).fetchone()

    assert query_result_after_deletion is None, (
        'Запись пользователя не была удалена. Проверьте работу функции: '
        f'{deleting_one_row_for_user.__name__}'
    )
