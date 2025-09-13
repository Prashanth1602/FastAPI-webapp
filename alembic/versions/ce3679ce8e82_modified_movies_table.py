"""modified movies table

Revision ID: ce3679ce8e82
Revises: 2cab17e07815
Create Date: 2025-09-13 13:39:25.915086

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce3679ce8e82'
down_revision: Union[str, None] = '2cab17e07815'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
