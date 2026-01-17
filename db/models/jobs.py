from datetime import datetime, timezone
import uuid
from typing import Optional
from db.enums import JobStatus, JobType
from sqlalchemy import Enum, String, CheckConstraint, ForeignKey, JSON
from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class JobsOrm(Base):
    __tablename__ = "jobs"
    __table_args__ = (
        CheckConstraint(
            "job_type IN ('metrics', 'normalize', 'anomalies')",
            name="ck_jobs_job_type",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    dataset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("datasets.id"),
        nullable=False,
        index=True,
    )
    job_type: Mapped[JobType] = mapped_column(
        String(20),
        nullable=False,
    )
    status: Mapped[JobStatus] = mapped_column(
        Enum(JobStatus),
        nullable=False,
    )
    params: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict
    )
    result_uri: Mapped[Optional[str]] = mapped_column(nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(
        nullable=True,
    )
    finished_at: Mapped[Optional[datetime]] = mapped_column(
        nullable=True,
    )