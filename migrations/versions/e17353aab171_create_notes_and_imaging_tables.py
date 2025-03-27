"""Create notes and imaging tables

Revision ID: e17353aab171
Revises: d04f4e6d9b72
Create Date: 2025-03-26 15:23:38.942589

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e17353aab171'
down_revision: Union[str, None] = 'd04f4e6d9b72'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('fax_files', sa.Column('patient_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_faxfiles_patients', 'fax_files', 'patients', ['patient_id'], ['id'])


def downgrade():
    op.drop_constraint('fk_faxfiles_patients', 'fax_files', type_='foreignkey')
    op.drop_column('fax_files', 'patient_id')
