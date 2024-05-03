from bot.request_to_url.request_to_url import get_request_url


def test_get_request_url():
    """Тест функции отправки запроса к тестируемому URL."""
    correct_url = 'https://www.google.com/'
    result = get_request_url(correct_url)
    assert isinstance(result, dict), (
        f'Возвращенный функцией {get_request_url.__name__} тип данных не '
        'соответствует ТЗ:\nфункция должна вернуть словарь, но вернула: '
        f'{type(result)}.\nУбедитесь, что функция '
        f'{get_request_url.__name__} возвращает правильных тип данных.'
    )
    assert all(key in result for key in ('status', 'responce')), (
        f'Функция {get_request_url.__name__} вернула словарь с ключами, '
        'которые не соответствуют ТЗ при запросе с корректным URL.\n'
        f'Убедитесь, что функция {get_request_url.__name__} работает правильно.'
    )
    assert result.get('status'), (
        f'Функция {get_request_url.__name__} при удачно get запросе к URL '
        'под ключем "status" должна вернуть значение True.'
    )

    incorrect_url = 'https://www.google-shmugal.com/'
    result = get_request_url(incorrect_url)
    assert isinstance(result, dict), (
        f'Возвращенный функцией {get_request_url.__name__} тип данных не '
        'соответствует ТЗ:\nфункция должна вернуть словарь, но вернула: '
        f'{type(result)}.\nУбедитесь, что функция '
        f'{get_request_url.__name__} возвращает правильных тип данных.'
    )
    assert all(key in result for key in ('status', 'message_error')), (
        f'Функция {get_request_url.__name__} вернула словарь с ключами, '
        'которые не соответствуют ТЗ при неудачном запросе.\n'
        f'Убедитесь, что функция {get_request_url.__name__} работает правильно.'
    )
    assert not result.get('status'), (
        f'Функция {get_request_url.__name__} при не удачном get запросе к URL '
        'под ключем "status" должна вернуть значение False.'
    )
