import uuid
from typing import Dict, Any

from pydantic import BaseModel, Field

from db.enums import JobType


class CreateJobSchema(BaseModel):
    dataset_id: uuid.UUID
    job_type: JobType
    params: Dict[str, Any] = Field(default_factory=dict)