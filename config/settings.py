import json
import os
from datetime import datetime
from pathlib import Path

import docker
from dotenv import load_dotenv
from ulid import ULID

load_dotenv()


def get_ip(containter_name):
    client = docker.DockerClient(containter_name)
    container = client.containers.get(containter_name)
    return container.attrs["NetworkSettings"]["IPAddress"]


base_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class Settings:
    """
    Settings class
    """

    api_debug: bool = os.getenv("API_DEBUG", "")
    api_name: str = os.getenv("API_NAME", "")
    api_host: str = os.getenv("API_HOST", "")
    api_port: int = os.getenv("API_PORT", "")
    api_version: str = os.getenv("API_VERSION", "")
    auth_key: str = os.getenv("AUTH_KEY", "")
    host_url: str = os.getenv("HOST_URL", "")
    db_url: str = os.getenv("DATABASE_URL", "")
    service_scheme: str = os.getenv("SERVICE_SCHEME", "")
    service_retry: int = os.getenv("SERVICE_RETRY", "")

    log_level: str = os.getenv("LOG_LEVEL", "")
    log_format: str = os.getenv("LOG_FORMAT", "")
    # log_file: str = os.getenv("LOG_FILE", "")
    max_bytes: int = os.getenv("MAX_BYTES", "")

    ASC_PATH: str = os.getenv("ASC_PATH", "")


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()