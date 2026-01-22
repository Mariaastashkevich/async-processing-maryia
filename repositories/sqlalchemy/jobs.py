import uuid

from sqlalchemy.orm import Session

from db.models.jobs import JobsOrm
from repositories.interfaces.jobs import JobRepository


class SqlAlchemyJobRepository(JobRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, job: JobsOrm) -> None:
        self.session.add(job)
        self.session.flush()

    def get(self, job_id: uuid.UUID) -> JobsOrm | None:
        return self.session.get(JobsOrm, job_id)

