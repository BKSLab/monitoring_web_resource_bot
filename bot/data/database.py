import sqlite3


def database_connection(db_name: str) -> sqlite3.Connection:
    """Создания подключения к базе данных."""

    try:
        connection = sqlite3.connect(f'{db_name}.db')
    except sqlite3.Error as error:
        return f'Ошибка при подключение к БД: {error}'
    return connection


def create_table(db_name: str, table_name: str) -> None:
    """Создание таблицы для хранения данных о ресурсах пользователей.."""

    connection = database_connection(db_name)
    sql_query = f'''
            CREATE TABLE IF NOT EXISTS {table_name}(
            id INTEGER PRIMARY KEY,
            url TEXT NOT NULL,
            tg_user_id INTEGER NOT NULL,
            CONSTRAINT constraint_name UNIQUE (url)
        );
        '''
    connection.cursor().execute(sql_query)
    connection.close()


def add_data_to_table(
    db_name: str, table_name: str, url: str, tg_user_id: int
):
    """Добавление новой записи об отслеживаемом ресурсе в таблицу."""

    connection = database_connection(db_name)
    sql_query = f'INSERT INTO {table_name} (url, tg_user_id) VALUES(?, ?);'
    try:
        connection.cursor().execute(sql_query, (url, tg_user_id))
        connection.commit()
        connection.close()
    except sqlite3.IntegrityError:
        return {
            'status': False,
            'message_error': f'url {url} уже существует в БД',
        }
    finally:
        if connection:
            connection.close()
    return {'status': True}


def exists_url(
    db_name: str,
    table_name: str,
    url: str,
    tg_user_id: int,
) -> bool:
    """Проверка наличия URL в БД."""
    connection = database_connection(db_name)
    sql_query = (
        f'SELECT EXISTS (SELECT * FROM {table_name} WHERE '
        '(url =? AND tg_user_id = ?))'
    )
    query_result = (
        connection.cursor().execute(sql_query, (url, tg_user_id)).fetchone()[0]
    )
    if connection:
        connection.close()
    return query_result


def get_all_rows(db_name: str, table_name: str) -> list[tuple[int, str, int]]:
    """
    Получение из таблицы всех записей об отслеживаемых
    ресурсах пользователей.
    """

    connection = database_connection(db_name)
    sql_query = f'SELECT * FROM {table_name};'
    query_result = connection.cursor().execute(sql_query).fetchall()
    if connection:
        connection.close()
    return query_result


def get_all_rows_for_user(
    db_name: str, table_name: str, tg_user_id: int
) -> list[tuple[int, str, int]]:
    """Получение всех записей об отслеживаемых пользователем ресурсах."""

    connection = database_connection(db_name)
    sql_query = f'SELECT * FROM {table_name} WHERE tg_user_id = ?;'
    query_result = (
        connection.cursor().execute(sql_query, (tg_user_id,)).fetchall()
    )
    if connection:
        connection.close()
    return query_result


def deleting_rows_for_user(
    db_name: str, table_name: str, tg_user_id: int
) -> None:
    """Удаление всех записей об отслеживаемых пользователем ресурсах."""

    connection = database_connection(db_name)
    sql_query = f'DELETE FROM {table_name} WHERE tg_user_id = ?;'
    connection.cursor().execute(sql_query, (tg_user_id,))
    connection.commit()
    if connection:
        connection.close()


def deleting_one_row_for_user(
    db_name: str,
    table_name: str,
    url: str,
    tg_user_id: int,
) -> None:
    """Удаление одной записи об отслеживаемом пользователем ресурсе."""

    connection = database_connection(db_name)
    sql_query = f'DELETE FROM {table_name} WHERE url = ? AND tg_user_id = ?;'
    connection.cursor().execute(sql_query, ((url, tg_user_id)))
    connection.commit()
    if connection:
        connection.close()
