# from pydantic import BaseSettings


# class Settings(BaseSettings):
#     app_name: str = "Smart CV Backend"
#     api_v1_str: str = "/api/v1"
#     debug: bool = True
#     database_url: str = "sqlite:///./smart_cv.db"

#     class Config:
#         env_file = ".env"


# settings = Settings()

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool

    HOST: str
    PORT: int

    GOOGLE_API_KEY: str = ""

    class Config:
        env_file = ".env"


settings = Settings()