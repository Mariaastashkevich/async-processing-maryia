import uuid
from typing import Protocol

from db.models.jobs import JobsOrm


class JobRepository(Protocol):
    def add(self, job: JobsOrm) -> None: ...
    def get(self, job_id: uuid.UUID) -> JobsOrm | None: ...