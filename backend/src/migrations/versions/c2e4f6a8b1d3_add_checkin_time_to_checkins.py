"""add checkin_time to checkins

Revision ID: c2e4f6a8b1d3
Revises: a3f8d2e1b7c9
Create Date: 2026-02-28 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "c2e4f6a8b1d3"
down_revision = "a3f8d2e1b7c9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "checkins",
        sa.Column("checkin_time", sa.Time(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("checkins", "checkin_time")
