from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    session_cookie_name: str = "skillway_session"
    session_max_age_seconds: int = 60 * 60 * 24 * 7
    session_cookie_samesite: str = "lax"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/ai_learning_platform"
    )
    openai_api_key: str | None = None

    @property
    def session_cookie_secure(self) -> bool:
        return self.app_env == "production"

    @property
    def allowed_cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
