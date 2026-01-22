import uuid

from fastapi import APIRouter, Depends
from api.deps import get_create_dataset_uc, get_get_dataset_uc
from schemas.dataset_schemas.create_dataset import CreateDatasetSchema
from schemas.dataset_schemas.read_dataset import ReadDatasetSchema
from schemas.job_schemas.create_job import CreateJobSchema
from schemas.job_schemas.read_job import ReadJobSchema
from use_cases.create_dataset_uc import CreateDatasetUseCase
from use_cases.create_job_uc import CreateJobUseCase
from use_cases.get_dataset_use_case import GetDatasetUseCase

router = APIRouter()

@router.post(
    "",
    response_model=ReadDatasetSchema,
    status_code=201,
)
def create_dataset(
        dataset: CreateDatasetSchema,
        use_case: CreateDatasetUseCase = Depends(get_create_dataset_uc),
):
    return use_case.execute(dataset)


@router.get(
    "/{dataset_id}",
    response_model=ReadDatasetSchema,
)
def get_dataset(
        dataset_id: uuid.UUID,
        use_case: GetDatasetUseCase = Depends(get_get_dataset_uc),
):
    return use_case.get(dataset_id)






