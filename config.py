import os
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings

templates = Jinja2Templates(directory="templates")


class Settings(BaseSettings):
    FASTAPI_APP: str = 'main:app'
    FASTAPI_APP_RELOAD: bool = True

    FASTAPI_LOG_LEVEL: str
    LOG_LEVEL: str
    HOST_URL: str
    HOST_PORT: int
    STRIPE_API_KEY: str
    STRIPE_WEBHOOK_URL: str
    STRIPE_WEBHOOK_SECRET: str

    class Config:
        env_nested_delimiter = '__'
        env_file = '.env'
        env_file_encoding = 'utf-8'


app_setting = Settings()


class LogConfiguration:
    logger_name: str = "Stripe Payment Gateway"
    logger_formatter: str = "%(asctime)s-%(levelname)s-%(name)s-%(process)d-%(pathname)s|%(lineno)s:: %(funcName)s|%(" \
                            "lineno)s:: %(message)s "
    roll_over: str = "MIDNIGHT"
    backup_count: int = 90
    log_file_base_name: str = "log"
    log_file_base_dir: str = f"{os.getcwd()}/logs"
