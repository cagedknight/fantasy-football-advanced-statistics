from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration, sourced entirely from the environment.

    Nothing here is hardcoded to a host or port, so the same image runs
    locally and in any deployment target without a code change.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = "local"
    port: int = 8000
    database_url: str = "postgresql+asyncpg://fantasy:fantasy@localhost:5432/fantasy"

    # Comma separated rather than a JSON list: hosting dashboards make plain
    # strings easy to set and JSON easy to get subtly wrong.
    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
