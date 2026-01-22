"""changed type of jobtype column

Revision ID: 508c02b623dc
Revises: e73ce0c191e1
Create Date: 2026-01-22 10:59:20.060235

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '508c02b623dc'
down_revision: Union[str, Sequence[str], None] = '64dfff8c929a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

jobtype_enum = sa.Enum(
    "metrics",
    "normalize",
    "anomalies",
    name="jobtype",
)


def upgrade() -> None:
    jobtype_enum.create(op.get_bind(), checkfirst=True)

    op.drop_constraint("ck_jobs_job_type",
                       "jobs",
                       type_="check"
                       )

    op.alter_column(
        "jobs",
        "job_type",
        existing_type=sa.VARCHAR(length=20),
        type_=jobtype_enum,
        postgresql_using="job_type::jobtype",
        nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "jobs",
        "job_type",
        existing_type=jobtype_enum,
        type_=sa.VARCHAR(length=20),
        nullable=False,
    )

    op.create_check_constraint(
        "ck_jobs_job_type",
        "jobs",
        sa.text("job_type IN ('metrics', 'normalize', 'anomalies')"),
    )

    jobtype_enum.drop(op.get_bind(), checkfirst=True)