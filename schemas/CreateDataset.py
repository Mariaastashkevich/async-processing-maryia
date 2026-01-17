from pydantic import BaseModel, Field

from db.enums import FileFormat


class CreateDatasetSchema(BaseModel):
    owner_id: str = Field(max_length=50)
    name: str = Field(max_length=100)
    format: FileFormat


