from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent

logger.debug("BASE_DIR: %s", BASE_DIR)


class Settings(BaseSettings):
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    S3_ENDPOINT_URL: str
    S3_REGION: str
    S3_DATASETS_BUCKET: str
    S3_JOB_RESULTS_BUCKET: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    STORAGE_TMP_DIR: ClassVar[Path] = BASE_DIR / "storage" / "tmp" / "jobs"
    STORAGE_UPLOADS_DIR: ClassVar[Path] = BASE_DIR / "storage" / "uploads"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()