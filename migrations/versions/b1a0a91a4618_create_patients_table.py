# migrations/versions/xxxxxxxxxxxx_create_patients_table.py
"""create patients table"""

from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision = 'b1a0a91a4618'       # Set this to whatever Alembic generated
down_revision = '413c54aa2d0d'  # Replace with your most recent existing migration ID
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'patients',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('uuid', sa.dialects.postgresql.UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True, unique=True),
        sa.Column('phone', sa.String(), nullable=True, unique=True),
        sa.Column('date_of_birth', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'))
    )

def downgrade():
    op.drop_table('patients')