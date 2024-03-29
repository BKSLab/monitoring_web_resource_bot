from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsTest(BaseSettings):
    """Класс конфигурации для тестовой базы данных."""

    table_name: SecretStr
    db_name: SecretStr

    model_config = SettingsConfigDict(
        env_file='.env.test', env_file_encoding='utf-8'
    )


config_db = SettingsTest()
