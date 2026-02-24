"""drop priority from relationships

Revision ID: a3f8d2e1b7c9
Revises: f5b8e9d2a3c4
Create Date: 2026-02-24 14:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a3f8d2e1b7c9"
down_revision: Union[str, Sequence[str], None] = "f5b8e9d2a3c4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remove the priority column from relationships — all caregivers are notified equally."""
    op.drop_column("relationships", "priority")


def downgrade() -> None:
    """Re-add priority column to relationships."""
    op.add_column(
        "relationships",
        sa.Column("priority", sa.Integer(), nullable=False, server_default="0"),
    )
