import os

from sqlalchemy.orm import Session
from db.enums import Status
from db.models.datasets import DatasetsOrm
from schemas.CreateDataset import CreateDatasetSchema
from services.settings import settings
from services.storage.storage_service import StorageService


class DatasetService:
    def __init__(self, session: Session, storage: StorageService):
        self.session = session
        self.storage = storage


    def create(self, data: CreateDatasetSchema) -> DatasetsOrm:
        bucket = settings.S3_DATASETS_BUCKET
        file_name = f"{data.name}.{data.format.value}"
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

        self.session.add(dataset)
        self.session.flush()
        return dataset




