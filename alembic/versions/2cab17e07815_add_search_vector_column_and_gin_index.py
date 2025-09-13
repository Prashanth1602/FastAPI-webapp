"""add search_vector column and GIN index

Revision ID: 2cab17e07815
Revises: f369f31d2029
Create Date: 2025-09-13 13:19:43.438326

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2cab17e07815'
down_revision: Union[str, None] = 'f369f31d2029'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add generated column
    op.execute("""
        ALTER TABLE movies 
        ADD COLUMN search_vector tsvector 
        GENERATED ALWAYS AS (
          to_tsvector(
            'english',
            coalesce(title, '') || ' ' || coalesce(genre, '') || ' ' || coalesce(description, '')
          )
        ) STORED;
    """)

    # Create GIN index
    op.execute("""
        CREATE INDEX idx_movies_search_vector 
        ON movies USING GIN (search_vector);
    """)


def downgrade() -> None:
    # Drop index first
    op.execute("DROP INDEX IF EXISTS idx_movies_search_vector;")

    # Drop column
    op.execute("ALTER TABLE movies DROP COLUMN IF EXISTS search_vector;")