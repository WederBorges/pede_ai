"""mudanças de regras

Revision ID: 46c4204de3f9
Revises: f2d1736301ae
Create Date: 2026-09-13 12:21:50.846158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46c4204de3f9'
down_revision: Union[str, Sequence[str], None] = 'f2d1736301ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
