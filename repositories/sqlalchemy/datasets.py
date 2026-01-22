import uuid

from sqlalchemy.orm import Session

from db.models.datasets import DatasetsOrm
from repositories.interfaces.datasets import DatasetRepository


class SqlAlchemyDatasetRepository(DatasetRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, dataset: DatasetsOrm) -> None:
        self.session.add(dataset)
        self.session.flush()

    def get(self, dataset_id: uuid.UUID) -> DatasetsOrm | None:
        return self.session.get(DatasetsOrm, dataset_id)



