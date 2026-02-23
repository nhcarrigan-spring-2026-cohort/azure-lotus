"""relationship based schema

Revision ID: b1d3f4a1c2e7
Revises: e85cacb6fae2
Create Date: 2026-02-23 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b1d3f4a1c2e7"
down_revision: Union[str, Sequence[str], None] = "e85cacb6fae2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("users", "roles")

    op.create_table(
        "relationships",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("senior_id", sa.Integer(), nullable=False),
        sa.Column("caregiver_id", sa.Integer(), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["senior_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["caregiver_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.add_column("checkins", sa.Column("relationship_id", sa.Integer(), nullable=False))
    op.add_column("checkins", sa.Column("status", sa.String(), nullable=False))
    op.add_column("checkins", sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_foreign_key(
        op.f("checkins_relationship_id_fkey"),
        "checkins",
        "relationships",
        ["relationship_id"],
        ["id"],
    )

    op.create_table(
        "alerts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("checkin_id", sa.Integer(), nullable=False),
        sa.Column("alert_type", sa.String(), nullable=False),
        sa.Column("resolved", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["checkin_id"], ["checkins.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.drop_index(op.f("ix_invitations_volunteer_email"), table_name="invitations")
    op.drop_index(op.f("ix_invitations_token"), table_name="invitations")
    op.drop_table("invitations")
    op.drop_table("senior_profiles")

    op.execute("DROP TYPE IF EXISTS invitationstatus")
    op.execute("DROP TYPE IF EXISTS checkinmethod")
    op.execute("DROP TYPE IF EXISTS checkinstatus")


def downgrade() -> None:
    op.create_table(
        "senior_profiles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("emergency_contact_phone", sa.String(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("medical_info", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("assigned_volunteer_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["assigned_volunteer_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )

    op.create_table(
        "invitations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("senior_id", sa.Integer(), nullable=False),
        sa.Column("invited_by", sa.Integer(), nullable=False),
        sa.Column("volunteer_email", sa.String(), nullable=False),
        sa.Column("token", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("accepted_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["invited_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["senior_id"], ["senior_profiles.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_invitations_token"), "invitations", ["token"], unique=True)
    op.create_index(
        op.f("ix_invitations_volunteer_email"),
        "invitations",
        ["volunteer_email"],
        unique=False,
    )

    op.drop_table("alerts")

    op.drop_constraint(op.f("checkins_relationship_id_fkey"), "checkins", type_="foreignkey")
    op.drop_column("checkins", "created_at")
    op.drop_column("checkins", "status")
    op.drop_column("checkins", "relationship_id")

    op.drop_table("relationships")

    op.add_column("users", sa.Column("roles", sa.JSON(), nullable=True))
