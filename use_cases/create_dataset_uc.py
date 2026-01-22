from db.models.datasets import DatasetsOrm
from schemas.dataset_schemas.create_dataset import CreateDatasetSchema
from services.dataset_service import DatasetService


class CreateDatasetUseCase:
    def __init__(self, service: DatasetService):
        self.service = service

    def execute(self, dataset: CreateDatasetSchema) -> DatasetsOrm:
        return self.service.create(dataset)
