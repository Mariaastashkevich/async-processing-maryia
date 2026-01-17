from datetime import datetime, timezone
import uuid
from typing import Optional
from db.enums import Status, FileFormat
from sqlalchemy import Enum, String, CheckConstraint
from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class DatasetsOrm(Base):
    __tablename__ = "datasets"

    __table_args__ = (
        CheckConstraint(
            "format IN ('csv', 'json', 'parquet')",
            name="ck_datasets_format",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[str] = mapped_column(
        String(45),
        nullable=False,
        index=True
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    status: Mapped[Status] = mapped_column(
        Enum(Status, name="datasetstatus"),
        nullable=False,
    )
    storage_uri: Mapped[str] = mapped_column(nullable=False)
    format: Mapped[FileFormat] = mapped_column(
        String(20),
        nullable=False,
    )
    size_bytes: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
