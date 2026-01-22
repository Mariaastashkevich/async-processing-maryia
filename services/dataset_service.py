import os
import uuid

from db.enums import Status
from db.models.datasets import DatasetsOrm
from repositories.interfaces.datasets import DatasetRepository
from schemas.dataset_schemas.create_dataset import CreateDatasetSchema
from services.settings import settings
from services.storage.storage_service import StorageService


class DatasetService:
    def __init__(self, storage: StorageService, repo: DatasetRepository):
        self.storage = storage
        self.repo = repo

    def create(self, data: CreateDatasetSchema) -> DatasetsOrm:
        bucket = settings.S3_DATASETS_BUCKET
        file_name = settings.STORAGE_UPLOADS_DIR / f"{data.name}.{data.format.value}"
        size_bytes = os.path.getsize(file_name)
        key = f"{data.owner_id}/{data.name}.{data.format.value}"

        dataset = DatasetsOrm(
            owner_id=data.owner_id,
            name=data.name,
            storage_uri=f"s3://{bucket}/{key}",
            format=data.format.value,
            size_bytes=size_bytes,
            status=Status.UPLOADED
        )

        self.storage.upload_file(
            bucket=bucket,
            key=key,
            file_name=file_name,
        )

        self.repo.add(dataset)
        return dataset

    def get_dataset(self, dataset_id: uuid.UUID) -> DatasetsOrm | None:
        return self.repo.get(dataset_id)





