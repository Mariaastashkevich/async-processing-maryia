from ports.job_runner import JobRunner
from workers.jobs import run_job

class CeleryJobRunner(JobRunner):
    def run(self, job_id: str) -> None:
        run_job.delay(job_id)