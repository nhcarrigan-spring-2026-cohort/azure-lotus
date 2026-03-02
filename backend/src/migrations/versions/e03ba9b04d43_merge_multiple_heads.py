"""merge multiple heads

Revision ID: e03ba9b04d43
Revises: b9c3e1d7f2a6, c2e4f6a8b1d3
Create Date: 2026-03-01 23:06:00.716045

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e03ba9b04d43'
down_revision: Union[str, Sequence[str], None] = ('b9c3e1d7f2a6', 'c2e4f6a8b1d3')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
