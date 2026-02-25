"""checkin senior based

Revision ID: f5b8e9d2a3c4
Revises: d4a7c2b9f8e1
Create Date: 2026-02-24 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "f5b8e9d2a3c4"
down_revision: Union[str, Sequence[str], None] = "d4a7c2b9f8e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Change checkins from relationship-based to senior-based."""
    
    # Add senior_id column (nullable initially)
    op.add_column(
        "checkins",
        sa.Column("senior_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    
    # Populate senior_id from relationships
    op.execute(
        """
        UPDATE checkins c
        SET senior_id = r.senior_id
        FROM relationships r
        WHERE c.relationship_id = r.id
        """
    )
    
    # Make senior_id non-nullable
    op.alter_column("checkins", "senior_id", nullable=False)
    
    # Drop relationship_id foreign key and column
    op.drop_constraint("checkins_relationship_id_fkey", "checkins", type_="foreignkey")
    op.drop_column("checkins", "relationship_id")
    
    # Add foreign key for senior_id
    op.create_foreign_key(
        "checkins_senior_id_fkey",
        "checkins",
        "users",
        ["senior_id"],
        ["id"],
    )


def downgrade() -> None:
    """Revert checkins from senior-based to relationship-based."""
    
    # Add relationship_id column (nullable initially)
    op.add_column(
        "checkins",
        sa.Column("relationship_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    
    # Populate relationship_id with the first (lowest priority) relationship for each senior
    # Note: This is a lossy conversion - we don't know which relationship the checkin was for
    op.execute(
        """
        UPDATE checkins c
        SET relationship_id = (
            SELECT r.id
            FROM relationships r
            WHERE r.senior_id = c.senior_id
            ORDER BY r.priority ASC
            LIMIT 1
        )
        """
    )
    
    # Make relationship_id non-nullable
    op.alter_column("checkins", "relationship_id", nullable=False)
    
    # Drop senior_id foreign key and column
    op.drop_constraint("checkins_senior_id_fkey", "checkins", type_="foreignkey")
    op.drop_column("checkins", "senior_id")
    
    # Add foreign key for relationship_id
    op.create_foreign_key(
        "checkins_relationship_id_fkey",
        "checkins",
        "relationships",
        ["relationship_id"],
        ["id"],
    )
