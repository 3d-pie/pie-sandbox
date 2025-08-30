"""empty baseline

Revision ID: 0001_initial
Revises: 
Create Date: 2025-08-30

This migration file is intentionally empty.  It marks the starting
point of the project's schema and can be used as a baseline for
future migrations.  Human developers should create subsequent
revisions under the ``migrations/versions`` directory using the
Alembic CLI.
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Empty upgrade to serve as a baseline."""
    pass


def downgrade() -> None:
    """Empty downgrade to serve as a baseline."""
    pass