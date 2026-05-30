from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database — set DATABASE_URL directly (Supabase) or use individual vars (local)
    database_url_override: str = Field(
        default="",
        validation_alias=AliasChoices("DATABASE_URL_OVERRIDE", "DATABASE_URL"),
    )
    postgres_user: str = "cleo"
    postgres_password: str = "cleo_pass"
    postgres_db: str = "cleo_db"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    # Qdrant — set QDRANT_URL + QDRANT_API_KEY for cloud, or use host/port for local
    qdrant_url: str = ""
    qdrant_api_key: str = ""
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "cleo_docs"

    # AI
    anthropic_api_key: str = ""
    voyage_api_key: str = ""

    # Voice
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""
    deepgram_api_key: str = ""
    elevenlabs_api_key: str = ""
    elevenlabs_voice_id: str = ""

    # App
    app_env: str = "development"
    base_url: str = "http://localhost:8000"

    @property
    def database_url(self) -> str:
        if self.database_url_override:
            url = self.database_url_override
            # Supabase gives postgres:// — asyncpg needs postgresql+asyncpg://
            if url.startswith("postgres://"):
                url = url.replace("postgres://", "postgresql+asyncpg://", 1)
            elif url.startswith("postgresql://"):
                url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
            return url
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def is_dev(self) -> bool:
        return self.app_env == "development"


settings = Settings()
