import uuid
from datetime import timezone, datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from db.enums import JobStatus
from schemas.job_schemas.create_job import CreateJobSchema
from schemas.job_schemas.read_job import ReadJobSchema
from api.deps import get_create_job_uc, get_get_job_uc
from use_cases.create_job_uc import CreateJobUseCase
from use_cases.get_job_uc import GetJobUseCase

router = APIRouter()


@router.post(
    "",
    response_model=ReadJobSchema,
    status_code=201,
)
def create_job(
        job: CreateJobSchema,
        use_case: CreateJobUseCase = Depends(get_create_job_uc),
):
    return use_case.execute(job)


@router.get(
    "/{job_id}",
    response_model=ReadJobSchema,
)
def get_job(
        job_id: uuid.UUID,
        use_case: GetJobUseCase = Depends(get_get_job_uc),
):
    return use_case.get(job_id)


@router.get(
    "/{job_id}/result",
)
def get_job_result(
        job_id: uuid.UUID,
        use_case: GetJobUseCase = Depends(get_get_job_uc),
):
    job = use_case.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.result_uri is None:
        raise HTTPException(status_code=404, detail="Result not found")
    if job.job_status != JobStatus.COMPLETED:
        raise HTTPException(status_code=409, detail="Job not completed")
    return {
        "result_uri": job.result_uri
    }


@router.post(
    "/{job_id}/cancel",
)
def cancel_job(
        job_id: uuid.UUID,
        use_case: GetJobUseCase = Depends(get_get_job_uc),
):
    job = use_case.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.job_status in (JobStatus.FAILED, JobStatus.COMPLETED):
        raise HTTPException(status_code=409, detail="Job cannot be cancelled")
    job.job_status = JobStatus.CANCELED
    job.finished_at = datetime.now(timezone.utc)
    return {
        "status": "Cancelled",
    }




