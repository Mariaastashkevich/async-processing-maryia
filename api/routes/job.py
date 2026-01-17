from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.deps import get_db_session, get_storage_service
from schemas.CreateDataset import CreateDatasetSchema
from schemas.ReadDataset import ReadDatasetSchema
from services.DatasetService import DatasetService
from services.storage.s3_client import S3Client
from services.storage.storage_service import StorageService

router = APIRouter()

@router.post(
    "",
    response_model=ReadDatasetSchema,
    status_code=201,
)
def create_dataset(
        dataset: CreateDatasetSchema,
        db_session: Session = Depends(get_db_session),
        storage: StorageService = Depends(get_storage_service)
):
    service = DatasetService(
        session=db_session,
        storage=storage
    )
    return service.create(dataset)





