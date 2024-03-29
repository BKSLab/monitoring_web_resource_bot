from dataclasses import dataclass


@dataclass
class TextMessage:
    """Данные для текстовых сообщений."""

    start_msg: str = (
        ', привет! Я небольшой бот, который помогает '
        'делать GET запросы к твоим web ресурсам.'
    )
    wrong_input_msg: str = (
        ', что-то пошло не так, ты вводишь не то, что требуется'
    )
