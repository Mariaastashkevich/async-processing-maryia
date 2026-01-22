import uuid
from typing import Protocol

from db.models.datasets import DatasetsOrm


class DatasetRepository(Protocol):
    def add(self, dataset: DatasetsOrm) -> None: ...
    def get(self, dataset_id: uuid.UUID) -> DatasetsOrm | None: ...


