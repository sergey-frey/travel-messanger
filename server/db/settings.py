import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from pydantic import (
    AmqpDsn,
    AnyHttpUrl,
    BaseSettings,
    PostgresDsn,
    validator,
)

load_dotenv()


class Settings(BaseSettings):

    API: str = "/api"
    RPC: str = "/rpc"
    DOCS: str = "/docs"
    STARTUP: str = "startup"
    SHUTDOWN: str = "shutdown"

    SECRET_KEY = "XXXXXXXXXX"

    NAME: str = "FastAPI Clean API"
    VERSION: str = "1.0"
    DESCRIPTION: str = "FastAPI Clean REST API"
    SECRET_OPENAI_KEY: str = os.environ.get("SECRET_OPENAI")
    SWAGGER_UI_PARAMETERS: Dict[str, Any] = {
        "displayRequestDuration": True,
        "filter": True,
    }

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls,
        value: str | List[str],  # noqa: N805, WPS110
    ) -> str | List[str]:
        if isinstance(value, str) and not value.startswith("["):
            return [i.strip() for i in value.split(",")]
        elif isinstance(value, (list, str)):
            return value

        raise ValueError(value)

    DATABASE_URI: PostgresDsn | None = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls,
        value: str | None,
        values: Dict[str, Any],  # noqa: N805, WPS110
    ) -> str:
        if isinstance(value, str):
            return value
        DB_HOST = os.environ.get("DB_HOST")
        DB_PORT = os.environ.get("DB_PORT")
        DB_USER = os.environ.get("DB_USER")
        DB_NAME = os.environ.get("DB_NAME")
        DB_PASSWORD = os.environ.get("DB_PASS")
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            path=f"/{DB_NAME}",
        )


    class Config(object):
        case_sensitive = True


settings = Settings()