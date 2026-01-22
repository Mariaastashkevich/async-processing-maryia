import uuid

from db.models.jobs import JobsOrm
from services.job_service import JobService


class GetJobUseCase:
    def __init__(self, service: JobService):
        self.service = service

    def get(self, job_id: uuid.UUID) -> JobsOrm | None:
        return self.service.get_job(job_id)
