"""add completed_at to checkins

Revision ID: b9c3e1d7f2a6
Revises: a3f8d2e1b7c9
Create Date: 2026-02-25 09:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b9c3e1d7f2a6"
down_revision: Union[str, Sequence[str], None] = "a3f8d2e1b7c9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "checkins",
        sa.Column("completed_at", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("checkins", "completed_at")
