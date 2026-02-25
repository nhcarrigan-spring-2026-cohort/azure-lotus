"""convert ids to uuid

Revision ID: d4a7c2b9f8e1
Revises: b1d3f4a1c2e7
Create Date: 2026-02-23 00:30:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "d4a7c2b9f8e1"
down_revision: Union[str, Sequence[str], None] = "b1d3f4a1c2e7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')

    op.add_column(
        "users",
        sa.Column(
            "id_uuid",
            postgresql.UUID(as_uuid=True),
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
    )

    op.add_column(
        "relationships",
        sa.Column(
            "id_uuid",
            postgresql.UUID(as_uuid=True),
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
    )
    op.add_column(
        "relationships",
        sa.Column("senior_id_uuid", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.add_column(
        "relationships",
        sa.Column("caregiver_id_uuid", postgresql.UUID(as_uuid=True), nullable=True),
    )

    op.add_column(
        "checkins",
        sa.Column(
            "id_uuid",
            postgresql.UUID(as_uuid=True),
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
    )
    op.add_column(
        "checkins",
        sa.Column("relationship_id_uuid", postgresql.UUID(as_uuid=True), nullable=True),
    )

    op.add_column(
        "alerts",
        sa.Column(
            "id_uuid",
            postgresql.UUID(as_uuid=True),
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
    )
    op.add_column(
        "alerts",
        sa.Column("checkin_id_uuid", postgresql.UUID(as_uuid=True), nullable=True),
    )

    op.execute(
        """
        UPDATE relationships r
        SET senior_id_uuid = u.id_uuid
        FROM users u
        WHERE r.senior_id = u.id
        """
    )
    op.execute(
        """
        UPDATE relationships r
        SET caregiver_id_uuid = u.id_uuid
        FROM users u
        WHERE r.caregiver_id = u.id
        """
    )
    op.execute(
        """
        UPDATE checkins c
        SET relationship_id_uuid = r.id_uuid
        FROM relationships r
        WHERE c.relationship_id = r.id
        """
    )
    op.execute(
        """
        UPDATE alerts a
        SET checkin_id_uuid = c.id_uuid
        FROM checkins c
        WHERE a.checkin_id = c.id
        """
    )

    op.alter_column("relationships", "senior_id_uuid", nullable=False)
    op.alter_column("relationships", "caregiver_id_uuid", nullable=False)
    op.alter_column("checkins", "relationship_id_uuid", nullable=False)
    op.alter_column("alerts", "checkin_id_uuid", nullable=False)

    op.drop_constraint("alerts_checkin_id_fkey", "alerts", type_="foreignkey")
    op.drop_constraint("checkins_relationship_id_fkey", "checkins", type_="foreignkey")
    op.drop_constraint("relationships_senior_id_fkey", "relationships", type_="foreignkey")
    op.drop_constraint("relationships_caregiver_id_fkey", "relationships", type_="foreignkey")

    op.drop_constraint("alerts_pkey", "alerts", type_="primary")
    op.drop_constraint("checkins_pkey", "checkins", type_="primary")
    op.drop_constraint("relationships_pkey", "relationships", type_="primary")
    op.drop_constraint("users_pkey", "users", type_="primary")

    op.drop_column("alerts", "checkin_id")
    op.drop_column("alerts", "id")
    op.alter_column("alerts", "id_uuid", new_column_name="id")
    op.alter_column("alerts", "checkin_id_uuid", new_column_name="checkin_id")

    op.drop_column("checkins", "relationship_id")
    op.drop_column("checkins", "id")
    op.alter_column("checkins", "id_uuid", new_column_name="id")
    op.alter_column("checkins", "relationship_id_uuid", new_column_name="relationship_id")

    op.drop_column("relationships", "senior_id")
    op.drop_column("relationships", "caregiver_id")
    op.drop_column("relationships", "id")
    op.alter_column("relationships", "id_uuid", new_column_name="id")
    op.alter_column("relationships", "senior_id_uuid", new_column_name="senior_id")
    op.alter_column("relationships", "caregiver_id_uuid", new_column_name="caregiver_id")

    op.drop_column("users", "id")
    op.alter_column("users", "id_uuid", new_column_name="id")

    op.create_primary_key("users_pkey", "users", ["id"])
    op.create_primary_key("relationships_pkey", "relationships", ["id"])
    op.create_primary_key("checkins_pkey", "checkins", ["id"])
    op.create_primary_key("alerts_pkey", "alerts", ["id"])

    op.create_foreign_key(
        "relationships_senior_id_fkey",
        "relationships",
        "users",
        ["senior_id"],
        ["id"],
    )
    op.create_foreign_key(
        "relationships_caregiver_id_fkey",
        "relationships",
        "users",
        ["caregiver_id"],
        ["id"],
    )
    op.create_foreign_key(
        "checkins_relationship_id_fkey",
        "checkins",
        "relationships",
        ["relationship_id"],
        ["id"],
    )
    op.create_foreign_key(
        "alerts_checkin_id_fkey",
        "alerts",
        "checkins",
        ["checkin_id"],
        ["id"],
    )


def downgrade() -> None:
    raise NotImplementedError("Downgrade not supported for UUID conversion migration")
