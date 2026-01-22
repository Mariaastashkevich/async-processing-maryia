from datetime import datetime
import uuid

from pydantic import BaseModel, Field

from db.enums import FileFormat, Status


class ReadDatasetSchema(BaseModel):
    id: uuid.UUID
    owner_id: str = Field(max_length=50)
    name: str = Field(max_length=100)
    format: FileFormat
    storage_uri: str
    size_bytes: int
    status: Status
    created_at: datetime

    class Config:
        from_attributes = True
