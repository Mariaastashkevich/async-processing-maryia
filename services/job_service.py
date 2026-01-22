import uuid

from db.enums import JobStatus
from db.models.jobs import JobsOrm
from repositories.interfaces.jobs import JobRepository
from schemas.job_schemas.create_job import CreateJobSchema
from services.storage.storage_service import StorageService
from services.settings import settings

class JobService:
    def __init__(self, repository: JobRepository):
        self.repository = repository

    def create(self, data: CreateJobSchema) -> JobsOrm:
        job = JobsOrm(
            dataset_id=data.dataset_id,
            job_type=data.job_type,
            params=data.params,
            job_status=JobStatus.PENDING,
            result_uri=None
        )

        self.repository.add(job)

        return job

    def get_job(self, job_id: uuid.UUID) -> JobsOrm | None:
        return self.repository.get(job_id)

    def mark_running(self):
        pass

    def mark_completed(self):
        pass

    def mark_failed(self):
        pass

    def mark_canceled(self):
        pass

