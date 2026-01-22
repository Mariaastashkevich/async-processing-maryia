import uuid
from datetime import datetime
from typing import Dict, Any, Optional

from pydantic import BaseModel, Field

from db.enums import JobType, JobStatus


class ReadJobSchema(BaseModel):
    id: uuid.UUID
    dataset_id: uuid.UUID
    job_type: JobType
    job_status: JobStatus
    params: Dict[str, Any] = Field(default_factory=dict)
    result_uri: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True