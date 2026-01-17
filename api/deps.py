from db.db_session_cm import db_session
from services.storage.s3_client import S3Client
from services.storage.storage_service import StorageService
from services.settings import settings

def get_db_session():
    with db_session() as session:
        yield session


def get_storage_service() -> StorageService:
    return StorageService(
        S3Client(
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
            region_name=settings.S3_REGION,
        )
    )

