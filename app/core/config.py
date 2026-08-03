from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool

    HOST: str
    PORT: int
    ALLOW_ORIGINS: str = Field(default="")

    GOOGLE_API_KEY: str = ""

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
    }

    @property
    def allow_origins(self) -> List[str]:
        if not self.ALLOW_ORIGINS:
            return []
        return [origin.strip() for origin in self.ALLOW_ORIGINS.split(",") if origin.strip()]


settings = Settings()
