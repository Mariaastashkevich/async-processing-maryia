from datetime import datetime, timezone
import uuid
from sqlalchemy import Enum, ForeignKey, JSON, Index
from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column

from db.enums import EventType


class JobEventsOrm(Base):
    __tablename__ = "job_events"
    __table_args__ = (
        Index(
            "ix_job_events_job_id_created_at",
            "job_id",
                    "created_at",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
    )
    event_type: Mapped[EventType] = mapped_column(
        Enum(EventType),
        nullable=False,
    )
    payload: Mapped[dict] = mapped_column(
        JSON,
        nullable=True,
        default=dict,
    )
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
