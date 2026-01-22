from db.models.jobs import JobsOrm
from ports.job_runner import JobRunner
from schemas.job_schemas.create_job import CreateJobSchema
from services.job_service import JobService
from workers.jobs import run_job


class CreateJobUseCase:
    def __init__(self, service: JobService, job_runner: JobRunner):
        self.service = service
        self.job_runner = job_runner

    def execute(self, data: CreateJobSchema) -> JobsOrm:
        job = self.service.create(data)
        self.job_runner.run(str(job.id))
        return job

