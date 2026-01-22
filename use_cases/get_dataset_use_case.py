import uuid

from sqlalchemy.orm import Session

from db.models.datasets import DatasetsOrm
from services.dataset_service import DatasetService


class GetDatasetUseCase:
    def __init__(self, service: DatasetService):
        self.service = service

    def get(self, dataset_id: uuid.UUID) -> DatasetsOrm | None:
        return self.service.get_dataset(dataset_id)