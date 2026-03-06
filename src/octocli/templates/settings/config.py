from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="app/settings/.env",
        extra="ignore",
    )

    db_user: str = "user"
    db_pass: str = "password"
    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_name: str = "template_core"


class SettingsPrefix(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="app/settings/.env",
        extra="ignore",
    )

    table_prefix: str = "core_"


class SettingsEngine(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="app/settings/.env",
        extra="ignore",
    )

    engine: str = "mysql"

    def get_updated_at(self):
        """Wich text to use for updated_at based on the engine."""
        if self.engine == "mysql":
            updated_at_text = "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
        else:
            updated_at_text = "CURRENT_TIMESTAMP"
        return updated_at_text


class SettingsRabbitMQ(SettingsPrefix):
    rabbit_host: str = "127.0.0.1"
    rabbit_port: int = 5672
    rabbit_user: str = "guest"
    rabbit_pass: str = "guest"
