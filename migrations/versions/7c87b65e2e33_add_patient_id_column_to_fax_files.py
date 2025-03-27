"""add patient_id column to fax_files

Revision ID: 7c87b65e2e33
Revises: e17353aab171
Create Date: 2025-03-26 15:40:05.774817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c87b65e2e33'
down_revision: Union[str, None] = 'e17353aab171'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
