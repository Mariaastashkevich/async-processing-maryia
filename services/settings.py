from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    S3_ACCESS_KEY_ID: str
    S3_SECRET_ACCESS_KEY: str
    S3_ENDPOINT_URL: str
    S3_REGION: str
    S3_DATASETS_BUCKET: str
    S3_JOB_RESULTS_BUCKET: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()