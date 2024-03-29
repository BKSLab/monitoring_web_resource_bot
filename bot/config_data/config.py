from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Клас конфигурации секретных данных для работы бота."""

    bot_token: SecretStr
    user_id_admin: SecretStr
    db_name: SecretStr
    table_name: SecretStr

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )


config = Settings()
