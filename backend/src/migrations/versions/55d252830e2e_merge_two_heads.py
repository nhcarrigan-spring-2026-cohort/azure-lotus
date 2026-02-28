"""merge two heads

Revision ID: 55d252830e2e
Revises: a3f8d2e1b7c9, e8ec1cc60474
Create Date: 2026-02-28 16:15:54.569011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55d252830e2e'
down_revision: Union[str, Sequence[str], None] = ('a3f8d2e1b7c9', 'e8ec1cc60474')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
