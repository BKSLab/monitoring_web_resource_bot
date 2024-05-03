from dataclasses import dataclass


class InlineButtonData:
    def __init__(self, text: str, callback_data: str):
        self.text = text
        self.callback_data = callback_data


@dataclass
class ButtonData:
    """Данные для создания inline кнопок."""

    show_my_resources: InlineButtonData = InlineButtonData(
        'Мои ресурсы', 'monitoring_resources'
    )
    test_all_resources: InlineButtonData = InlineButtonData(
        'Тест всех ресурсов', 'test_all_resources'
    )
    add_resource: InlineButtonData = InlineButtonData(
        'Добавить ресурс', 'add_resource'
    )
    add: InlineButtonData = InlineButtonData('Добавить', 'add')
    back_to_main: InlineButtonData = InlineButtonData(
        'На главную', 'back_to_main'
    )
    delete_all_resources: InlineButtonData = InlineButtonData(
        'Удалить все URL', 'delete_del_allresources'
    )
