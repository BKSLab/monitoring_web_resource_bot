from typing import Union

import requests


def get_request_url(url) -> dict[str, Union[str, requests.Response]]:
    try:
        responce = requests.get(url)
    except requests.RequestException as error:
        return {
            'status': False,
            'message_error': str(error),
        }
    return {
        'status': True,
        'responce': responce,
    }
