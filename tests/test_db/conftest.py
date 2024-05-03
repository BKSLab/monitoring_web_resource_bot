import os
import sqlite3

import pytest
from config_for_db import config_db
from utils import resource_data


@pytest.fixture(scope='module')
def db_session():
    """Подготовка базы данных для тестов."""
    try:
        db_name = f'{config_db.db_name_test.get_secret_value()}.db'
        connection = sqlite3.connect(db_name)
        connection.isolation_level = None
    except sqlite3.Error as error:
        return f'Ошибка при подключение к БД: {error}'

    db_session = connection.cursor()
    yield db_session
    sql_query = (
        f'DROP TABLE IF EXISTS {config_db.table_name_test.get_secret_value()};'
    )
    db_session.execute(sql_query)
    if connection:
        connection.close()
    os.remove(f'{config_db.db_name_test.get_secret_value()}.db')


@pytest.fixture()
def insert_records_in_table(db_session: sqlite3.Cursor):
    """Наполнение базы данных тестовыми данными."""
    table_name = config_db.table_name_test.get_secret_value()
    sql_query = f'DELETE FROM {table_name};'
    db_session.execute(sql_query)
    sql_query = f'INSERT INTO {table_name} (url, tg_user_id) VALUES(?, ?);'
    db_session.executemany(sql_query, resource_data)
    yield
