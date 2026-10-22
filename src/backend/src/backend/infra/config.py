import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "")
    jwt_secret: str = field(default_factory=lambda: os.environ["JWT_SECRET"])
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    crypt_secret: str = field(default_factory=lambda: os.environ["CRYPTO_SECRET"])
    diff_bot_api_token: str = field(default_factory=lambda: os.environ["DIFF_BOT_API_TOKEN"])
    agni_app_url: str = field(default_factory=lambda: os.environ["AGNI_APP_URL"])


def get_settings() -> Settings:
    return Settings()