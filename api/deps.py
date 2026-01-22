from db.db_session_cm import db_session
from job_runners.celery_runner import CeleryJobRunner
from repositories.interfaces.datasets import DatasetRepository
from repositories.sqlalchemy.datasets import SqlAlchemyDatasetRepository
from repositories.sqlalchemy.jobs import SqlAlchemyJobRepository
from services.dataset_service import DatasetService
from services.job_service import JobService
from services.storage.s3_client import S3Client
from services.storage.storage_service import StorageService
from services.settings import settings
from use_cases.create_dataset_uc import CreateDatasetUseCase
from sqlalchemy.orm import Session
from fastapi import Depends

from use_cases.create_job_uc import CreateJobUseCase
from use_cases.get_dataset_use_case import GetDatasetUseCase
from use_cases.get_job_uc import GetJobUseCase


def get_db_session():
    with db_session() as session:
        yield session


def get_storage_service():
    return StorageService(
        S3Client(
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.MINIO_ROOT_USER,
            aws_secret_access_key=settings.MINIO_ROOT_PASSWORD,
            region_name=settings.S3_REGION,
        ),
        temp_dir=settings.STORAGE_TMP_DIR,
    )


def get_create_dataset_uc(
        session: Session = Depends(get_db_session),
        storage: StorageService = Depends(get_storage_service)
):
    repo = SqlAlchemyDatasetRepository(session=session)
    service = DatasetService(
        repo=repo,
        storage=storage,
    )
    return CreateDatasetUseCase(service=service)


def get_get_dataset_uc(
        session: Session = Depends(get_db_session),
        storage: StorageService = Depends(get_storage_service)
):
    repo = SqlAlchemyDatasetRepository(session=session)
    service = DatasetService(
        repo=repo,
        storage=storage,
    )
    return GetDatasetUseCase(service=service)


def get_create_job_uc(
        session: Session = Depends(get_db_session),
):
    repo = SqlAlchemyJobRepository(session=session)
    service = JobService(
        repository=repo,
    )
    celery_runner = CeleryJobRunner()
    return CreateJobUseCase(
        service=service,
        job_runner=celery_runner
    )


def get_get_job_uc(
        session: Session = Depends(get_db_session),
):
    repo = SqlAlchemyJobRepository(session=session)
    service = JobService(
        repository=repo,
    )
    return GetJobUseCase(service=service)


