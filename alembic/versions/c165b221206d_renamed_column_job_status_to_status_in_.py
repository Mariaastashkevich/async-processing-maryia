"""renamed column job_status to status in datasets

Revision ID: c165b221206d
Revises: 508c02b623dc
Create Date: 2026-01-22 12:45:52.641661

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c165b221206d'
down_revision: Union[str, Sequence[str], None] = '508c02b623dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "datasets",
        "job_status",
        new_column_name="status",
        existing_type=sa.Enum('UPLOADED', 'VALIDATING', 'READY', 'FAILED', name='datasetstatus'),
        nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "datasets",
        "status",
        new_column_name="job_status",
        existing_type=sa.Enum('UPLOADED', 'VALIDATING', 'READY', 'FAILED', name='datasetstatus'),
        nullable=False,
    )
